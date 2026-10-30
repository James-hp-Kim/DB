"""Persona-first contracts: fail closed across library, CLI and MCP."""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from mcp_server import dispatch,TOOLS

class PersonaGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='persona-검증-')
        self.path=Path(self.tmp.name)
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':str(self.path/'contexts')})
        self.env.start(); os.environ.pop('EXPERT_PRIVATE_DIR',None)
        self.qa=kb.available('품질보증',limit=1)['personas'][0]['context']
        self.data=kb.available('data-analyst',limit=1)['personas'][0]['context']

    def tearDown(self):
        self.env.stop(); self.tmp.cleanup()

    def calls(self,context=None):
        return [lambda:kb.lookup('MSA',context=context), lambda:kb.read(['quality:msa'],context=context),lambda:kb.sources(['nist-handbook'],context=context)]

    def test_missing_forged_and_id_only_rejected_before_db_open(self):
        with patch.object(kb,'connect',side_effect=AssertionError('DB opened before gate')):
            for context in (None,'quality-assurance','0'*24,'../secret',''):
                for call in self.calls(context):
                    with self.assertRaises(ValueError): call()

    def test_search_keywords_pagination_and_no_match(self):
        self.assertEqual(kb.available('QA')['personas'][0]['id'],'quality-assurance')
        self.assertEqual(kb.available('데이터')['personas'][0]['id'],'data-analyst')
        self.assertEqual(kb.available('존재하지않는역할')['personas'],[])
        first=kb.available('전문가',limit=1)
        second=kb.available('전문가',limit=1,offset=first['next_offset'])
        self.assertNotEqual(first['personas'][0]['id'],second['personas'][0]['id'])
        for bad in ('',None,'a'*121):
            with self.assertRaises(ValueError): kb.available(bad)
        with self.assertRaises(ValueError): kb.available('QA',limit=6)

    def test_receipt_reuse_expiry_catalog_change_foreign_root(self):
        for _ in range(2): self.assertTrue(kb.lookup('MSA',context=self.qa)['matches'])
        path=kb.context_directory()/(self.qa+'.json'); original=kb.load(path)
        for update in ({'expires':time.time()-1},{'catalog_sha256':'stale'},{'root':'elsewhere'},{'persona':'missing'}):
            path.write_text(json.dumps({**original,**update}),encoding='utf-8')
            for call in self.calls(self.qa):
                with self.assertRaises(ValueError): call()

    def test_source_bound_to_selected_packs(self):
        sets={}
        for pack in ('common','quality'):
            records=[json.loads(line) for line in (SKILL/f'packs/{pack}/records.jsonl').read_text(encoding='utf-8').splitlines()]
            sets[pack]={sid for record in records for sid in record['source_ids']}
        exclusive=next(iter(sets['quality']-sets['common']))
        with self.assertRaises(ValueError): kb.sources([exclusive],context=self.data)
        self.assertTrue(kb.sources([exclusive],context=self.data,packs=['quality'])['sources'])
        with self.assertRaises(ValueError): kb.read(['quality:msa'],context=self.data)
        with self.assertRaises(ValueError): kb.lookup('x',context=self.qa,packs=['private'])
        with self.assertRaises(ValueError): kb.sources([exclusive],context=self.qa,packs=['common'])

    def test_private_sources_explicit_only(self):
        note=self.path/'note.txt'; note.write_text('개인 근거',encoding='utf-8')
        store=self.path/'private'; info=kb.ingest_note(note,store,'개인 근거')
        os.environ['EXPERT_PRIVATE_DIR']=str(store)
        with self.assertRaises(ValueError): kb.sources([info['source_id']],context=self.qa)
        self.assertTrue(kb.sources([info['source_id']],context=self.qa,include_private=True)['sources'])

    def test_mcp_cannot_skip_search_or_supply_persona(self):
        state={'ready':True}
        args={'expert_lookup':{'query':'MSA'},'expert_read':{'ids':['quality:msa']},'expert_source':{'ids':['anything']}}
        for name,values in args.items():
            for invalid in ({}, {'persona':'quality-assurance'}, {'context':'0'*24}):
                result=dispatch({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':name,'arguments':{**values,**invalid}}},state)
                self.assertTrue('error' in result or result['result']['isError'])
        for tool in TOOLS[1:]: self.assertIn('context',tool['inputSchema']['required'])

    def test_cli_gate_and_search_flow(self):
        prefix=[sys.executable,'-B','-X','utf8',str(SKILL/'scripts/expert.py')]
        for args in (['lookup','MSA'],['read','quality:msa'],['source','anything'],['lookup','MSA','--persona','quality-assurance']):
            result=subprocess.run(prefix+args,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,2)
        found=subprocess.run(prefix+['catalog','품질보증','--limit','1'],capture_output=True,text=True,encoding='utf-8',check=True)
        context=json.loads(found.stdout)['personas'][0]['context']
        result=subprocess.run(prefix+['lookup','MSA','--context',context],capture_output=True,text=True,encoding='utf-8',check=True)
        self.assertEqual(json.loads(result.stdout)['persona'],'quality-assurance')

    def test_new_persona_search_and_invalid_defaults(self):
        catalog=kb.catalog()
        catalog['reliability-review']={**catalog['quality-assurance'],'label':'신규 검증 역할','keywords':['내구 검토']}
        with patch.object(kb,'catalog',return_value=catalog):
            found=kb.available('내구 검토')['personas'][0]
            self.assertEqual(found['id'],'reliability-review')
            self.assertTrue(kb.lookup('MSA',context=found['context'])['matches'])
        catalog['reliability-review']['default_packs']=['not-allowed']
        with patch.object(kb,'load',return_value=catalog):
            with self.assertRaises(ValueError): kb.catalog()

if __name__=='__main__': unittest.main(verbosity=2)
