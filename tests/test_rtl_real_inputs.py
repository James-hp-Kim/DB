"""Public RTL/archived tool logs and persona-before-I/O regression, not silicon validation."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from input_reference import reference_input
from mcp_server import dispatch
from qa_core import dump,digest


class RealInputTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='RTL 실제 공개 자료 ')
        self.path=Path(self.temp.name)
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':str(self.path/'contexts')})
        self.env.start()
        self.context=kb.available('chip-design-verification',limit=1)['personas'][0]['context']
        prefix='semiconductor-codex-kit/plugins/chip-evidence/evidence/'
        self.members={
          'picorv32.v':'references/sources/YosysHQ/picorv32/picorv32.v',
          'baseline-directed-w0.log':'validation/logs/baseline-directed-w0.log',
          'M01_sub_as_add-directed-w0.log':'validation/logs/M01_sub_as_add-directed-w0.log',
          'baseline-synthesis.log':'validation/logs/baseline-synthesis.log'}
        with zipfile.ZipFile(BASE/'third_party/semiconductor-evidence-20261029.zip') as archive:
            for name,rel in self.members.items():
                (self.path/name).write_bytes(archive.read(prefix+rel))

    def tearDown(self):
        self.env.stop(); self.temp.cleanup()

    def verify_result(self,path,result,expected):
        payload=dump(result)
        self.assertLessEqual(len(payload),2500)
        self.assertEqual(result['selected_pack'],'rtl')
        self.assertEqual(result['retrieval']['packs'],['rtl'])
        self.assertLessEqual(len(result['retrieval']['matches']),3)
        self.assertIn(expected,[x['id'] for x in result['retrieval']['matches']])
        self.assertNotIn(str(path),payload)
        self.assertNotIn('module picorv32',payload)
        self.assertNotIn('MISMATCH word=',payload)
        for hit in result['retrieval']['matches']:
            self.assertNotIn('body',hit)
            self.assertIsInstance(hit['sections'],list)
        self.assertEqual(result['input']['sha256'],digest(path))

    def test_actual_public_rtl_and_synthesis_log(self):
        for name in ('picorv32.v','baseline-synthesis.log'):
            path=self.path/name; before=digest(path)
            result=reference_input(path,context=self.context,max_chars=2500)
            self.verify_result(path,result,'rtl:c04')
            self.assertEqual(digest(path),before)

    def test_actual_pass_fail_logs_find_scoreboard_without_query(self):
        for name in ('baseline-directed-w0.log','M01_sub_as_add-directed-w0.log'):
            path=self.path/name
            result=reference_input(path,context=self.context,max_chars=2500)
            self.verify_result(path,result,'rtl:c11')
            self.assertEqual(result['signals'][0]['topic'],'verification-result')

    def test_selected_sections_sources_and_scope(self):
        found=reference_input(self.path/'M01_sub_as_add-directed-w0.log',context=self.context,max_chars=2500)
        self.assertIn('rtl:c11',[x['id'] for x in found['retrieval']['matches']])
        page=kb.read(['rtl:c11'],context=self.context,sections=['conditions','verification','limits'],max_chars=2500)
        self.assertEqual({x['section'] for x in page['items']},{'conditions','verification','limits'})
        self.assertEqual({x['id'] for x in page['items']},{'rtl:c11'})
        self.assertLessEqual(len(dump(page)),2500)
        source_ids=list(dict.fromkeys(s for x in page['items'] for s in x['sources']))
        result=kb.sources(source_ids,context=self.context,max_chars=3000)
        self.assertEqual(len(result['sources']),len(source_ids))
        with self.assertRaises(ValueError):kb.lookup('MSA',context=self.context,packs=['quality'])

    def test_no_persona_zero_database_connections_and_input_io(self):
        path=self.path/'picorv32.v'
        expired=kb.available('chip-design-verification',limit=1)['personas'][0]['context']
        rp=kb.context_directory()/(expired+'.json'); receipt=kb.load(rp);receipt['expires']=time.time()-1
        rp.write_text(dump(receipt),encoding='utf-8')
        original_stat=Path.stat; original_open=Path.open
        stats=[]; opens=[]
        def observe_stat(p,*args,**kwargs):
            if p==path:stats.append(str(p))
            return original_stat(p,*args,**kwargs)
        def observe_open(p,*args,**kwargs):
            if p==path:opens.append(str(p))
            return original_open(p,*args,**kwargs)
        with patch.object(kb,'connect',wraps=kb.connect) as connections,patch.object(Path,'stat',observe_stat),patch.object(Path,'open',observe_open):
            for context in (None,'','chip-design-verification','0'*24,expired):
                calls=[lambda:kb.lookup('FIFO',context=context),
                       lambda:kb.read(['rtl:c09'],context=context),
                       lambda:kb.sources(['rtl-s04'],context=context),
                       lambda:reference_input(path,context=context)]
                for call in calls:
                    with self.assertRaises(ValueError):call()
            self.assertEqual(connections.call_count,0)
        self.assertEqual(stats,[])
        self.assertEqual(opens,[])

    def test_wrong_persona_no_input_io(self):
        context=kb.available('quality-assurance',limit=1)['personas'][0]['context']
        target=self.path/'picorv32.v'; original_stat=Path.stat
        def guard_input(p,*args,**kwargs):
            if p==target:raise AssertionError('Unexpected input stat')
            return original_stat(p,*args,**kwargs)
        with patch.object(Path,'stat',guard_input),patch.object(kb,'connect',side_effect=AssertionError('Unexpected DB connect')):
            with self.assertRaises(ValueError):reference_input(target,context=context)

    def test_mcp_missing_or_invalid_context_does_not_call_db(self):
        state={}
        dispatch({'jsonrpc':'2.0','id':0,'method':'initialize','params':{'protocolVersion':'2025-11-25'}},state)
        dispatch({'jsonrpc':'2.0','method':'notifications/initialized'},state)
        cases={'expert_lookup':{'query':'FIFO'},'expert_read':{'ids':['rtl:c09']},
               'expert_source':{'ids':['rtl-s04']},'expert_reference_input':{'file':str(self.path/'picorv32.v')}}
        with patch.object(kb,'connect',wraps=kb.connect) as connections:
            for name,args in cases.items():
                for scope in ({},{'context':None},{'context':'0'*24},{'persona':'chip-design-verification'}):
                    result=dispatch({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':name,'arguments':{**args,**scope}}},state)
                    self.assertTrue('error' in result or result['result']['isError'])
            self.assertEqual(connections.call_count,0)

    def test_cli_requires_context_and_real_log_works(self):
        cli=[sys.executable,'-B','-X','utf8',str(SKILL/'scripts/expert.py')]
        for args in (['lookup','FIFO'],['read','rtl:c09'],['source','rtl-s04'],['reference-input',str(self.path/'picorv32.v')]):
            r=subprocess.run(cli+args,capture_output=True,encoding='utf-8')
            self.assertEqual(r.returncode,2)
            self.assertEqual(r.stdout,'')
        r=subprocess.run(cli+['reference-input',str(self.path/'M01_sub_as_add-directed-w0.log'),'--context',self.context,'--max-chars','2500'],capture_output=True,encoding='utf-8',check=True)
        self.verify_result(self.path/'M01_sub_as_add-directed-w0.log',json.loads(r.stdout),'rtl:c11')

    def test_unknown_input_no_database_connection(self):
        path=self.path/'unknown.txt';path.write_text('unrelated noise without recognized topics',encoding='utf-8')
        with patch.object(kb,'connect',wraps=kb.connect) as connections:
            result=reference_input(path,context=self.context)
            self.assertIn('gap',result)
            self.assertEqual(connections.call_count,0)


if __name__=='__main__':unittest.main(verbosity=2)
