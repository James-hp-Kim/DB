"""Semiconductor evidence, scope, input routing and bounded retrieval contracts."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
SKILL = BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0, str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump, digest
from semiconductor_reference import reference
from mcp_server import dispatch

CASES = [('누설전류 원인','semiconductor:c06'),
         ('단일 소자 누설 분해','semiconductor:e01'),
         ('DRAM retention','semiconductor:e03'),
         ('HBM 대역폭','semiconductor:k06'),
         ('IGZO retention','semiconductor:n32'),
         ('high-Vt','semiconductor:l01'),
         ('동적전력','semiconductor:k01'),
         ('record_id','semiconductor:f01'),
         ('소자 개발','semiconductor:j01')]


class SemiconductorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='반도체 시험 ')
        self.env = patch.dict(os.environ, {'EXPERT_CONTEXT_DIR': self.tmp.name})
        self.env.start()
        self.context = kb.available('반도체기초전문가',limit=1)['personas'][0]['context']

    def tearDown(self):
        self.env.stop(); self.tmp.cleanup()

    def test_inventory_and_migration_completeness(self):
        rows = [json.loads(x) for x in (SKILL/'packs/semiconductor/records.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(rows),151)
        manifest = kb.load(BASE/'docs/SEMICONDUCTOR_IMPORT.json')
        self.assertEqual(len(manifest['mapping']),185)
        self.assertEqual(sum('record_id' in r for r in manifest['mapping']),152)
        for r in rows:
            self.assertTrue(r['sections']['conditions'])
            self.assertTrue(r['sections']['limits'])
        self.assertTrue(kb.read(['common:zero-failure-upper'],context=self.context,packs=['common'])['items'])

    def test_nine_known_queries(self):
        for query, expected in CASES:
            result = kb.lookup(query,context=self.context)
            self.assertIn(expected,[r['id'] for r in result['matches']],query)
            self.assertEqual(result['packs'],['semiconductor'])
            self.assertNotIn('detail',result['matches'][0])

    def test_condition_and_evidence_boundaries(self):
        result = kb.read(['semiconductor:n32'],context=self.context,sections=['conditions','limits'])
        self.assertIn('14',dump(result))
        result = kb.read(['semiconductor:e01'],context=self.context,sections=['limits'])
        self.assertIn('미실행',dump(result))
        result = kb.read(['semiconductor:k03'],context=self.context,sections=['verification'])
        self.assertIn('실측이 아님',dump(result))

    def test_sources_and_disallowed_scope(self):
        rows = [json.loads(x) for x in (SKILL/'packs/semiconductor/records.jsonl').read_text(encoding='utf-8').splitlines()]
        for sid in {s for r in rows for s in r['source_ids']}:
            self.assertTrue(kb.sources([sid],context=self.context)['sources'][0]['url'])
        with self.assertRaises(ValueError): kb.lookup('MSA',context=self.context,packs=['quality'])
        with self.assertRaises(ValueError): kb.read(['quality:msa'],context=self.context)
        qa = kb.available('quality-assurance',limit=1)['personas'][0]['context']
        with self.assertRaises(ValueError): kb.read(['semiconductor:e01'],context=qa)

    def test_caps_and_selected_sections(self):
        for cap in [1200,2000,3500]:
            self.assertLessEqual(len(dump(kb.lookup('누설전류 DRAM HBM',context=self.context,max_chars=cap))),cap)
        page=kb.read(['semiconductor:c06'],context=self.context,sections=['limits'],max_chars=2000)
        self.assertEqual(len(page['items']),1)
        self.assertNotIn('케이블',dump(page))

    def test_file_routing_does_not_return_or_store_raw_data(self):
        p=Path(self.tmp.name)/'한글 입력 자료.csv'
        p.write_text('Vgs,Vds,Ioff,private_note\n0,1,1e-9,DO_NOT_ECHO_abcdef\n',encoding='utf-8-sig')
        before=digest(p)
        result=reference(p,self.context,max_chars=2500)
        self.assertLessEqual(len(dump(result)),2500)
        self.assertNotIn('DO_NOT_ECHO_abcdef',dump(result))
        self.assertIn('semiconductor:e01',[r['id'] for r in result['retrieval']['matches']])
        self.assertEqual(before,digest(p))
        self.assertEqual(result['signals'][0]['lines'],[1])

    def test_file_gate_and_invalid_files(self):
        with self.assertRaises(ValueError): reference('missing.csv',None)
        qa=kb.available('quality-assurance',limit=1)['personas'][0]['context']
        with self.assertRaises(ValueError): reference('missing.csv',qa)
        p=Path(self.tmp.name)/'input.txt'
        p.write_bytes(b'\x00')
        with self.assertRaises(ValueError): reference(p,self.context)
        p.write_bytes(b'x'*(2*1024*1024+1))
        with self.assertRaises(ValueError): reference(p,self.context)
        p.write_text('unrelated text',encoding='utf-8')
        self.assertIn('gap',reference(p,self.context))
        self.assertIn('retrieval',reference(p,self.context,query='동적전력'))

    def test_cli_and_mcp_same_scope(self):
        args={'query':'단일 소자 누설 분해','context':self.context}
        direct=kb.lookup(**args)
        state={}
        dispatch({'jsonrpc':'2.0','id':0,'method':'initialize','params':{'protocolVersion':'2025-11-25'}},state)
        dispatch({'jsonrpc':'2.0','method':'notifications/initialized'},state)
        response=dispatch({'jsonrpc':'2.0','id':1,'method':'tools/call',
            'params':{'name':'expert_lookup','arguments':args}}, state)
        self.assertEqual(json.loads(response['result']['content'][0]['text']),direct)
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(SKILL/'scripts/expert.py'),'lookup',args['query'],'--context',self.context],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(json.loads(run.stdout),direct)


if __name__=='__main__': unittest.main()
