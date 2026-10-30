"""Backend extension: scoped, bounded retrieval plus genuine failure evidence."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump
from mcp_server import dispatch

CASES=[
 ('DB 연결 풀 고갈','pool-exhaustion'),('앱 증설 워커 연결수','pool-budget'),
 ('느린 쿼리 인덱스','slow-query'),('EXPLAIN ANALYZE','explain'),
 ('트래픽 급증 과부하','overload'),('Redis 캐시 TTL','cache-storm'),
 ('재시도 deadline','retry'),('배포 롤백 호환성','rollback'),
 ('잠금 blocking transaction','blocking'),('백업 복원 RPO','restore'),
 ('p95 동일 조건 비교','latency-comparison'),('7/320 시간초과 재현','lab-limit'),
 ('로그 JSON 입력 자료','intake'),('50만 SQLite 실험','lab-results')]

class BackendTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='backend-gate-')
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':self.tmp.name})
        self.env.start()
        self.choice=kb.available('백엔드',limit=1)
        self.context=self.choice['personas'][0]['context']
    def tearDown(self): self.env.stop(); self.tmp.cleanup()
    def test_persona_names(self):
        for query in ('백엔드','벡엔드','backend','backend-expert'):
            self.assertEqual(kb.available(query,limit=1)['personas'][0]['id'],'backend-expert')
        self.assertEqual(kb.catalog()['backend-expert']['default_packs'],['backend','common'])
    def test_backend_inventory(self):
        records=[json.loads(line) for line in (SKILL/'packs/backend/records.jsonl').read_text(encoding='utf-8').splitlines()]
        inventory=json.loads((BASE/'docs/RELEASE_INVENTORY.json').read_text(encoding='utf-8'))
        expected=inventory['packs']['backend']
        self.assertEqual(len(records),expected)
        self.assertEqual(len({r['id'] for r in records}),expected)
        for record in records:
            self.assertTrue(record['sections']['conditions'])
            self.assertTrue(record['sections']['limits'])
            self.assertTrue(kb.sources(record['source_ids'],context=self.context)['sources'])
    def test_expected_top_two(self):
        for query,rid in CASES:
            with self.subTest(query=query):
                result=kb.lookup(query,context=self.context,limit=2,max_chars=1800)
                self.assertIn('backend:'+rid,[r['id'] for r in result['matches']])
                self.assertLessEqual(len(dump(result)),1800)
                self.assertLessEqual(len(result['matches']),2)
                self.assertNotIn('sections_body',dump(result))
    def test_selected_sections_and_failure_preserved(self):
        result=kb.read(['backend:pool-exhaustion'],context=self.context,sections=['conditions','procedure','limits'],max_chars=3000)
        self.assertEqual([r['section'] for r in result['items']],['conditions','procedure','limits'])
        self.assertLessEqual(len(dump(result)),3000)
        self.assertTrue(all(r['next_offset'] is None for r in result['items']))
        failure=kb.read(['backend:lab-limit'],context=self.context,sections=['conditions','procedure','limits'],max_chars=3000)
        self.assertIn('원인',dump(failure))
        self.assertIn('exit1',dump(failure))
    def test_scope_rejects_other_personas(self):
        with self.assertRaises(ValueError): kb.lookup('MSA',context=self.context,packs=['quality'])
        with self.assertRaises(ValueError): kb.read(['quality:msa'],context=self.context)
        with self.assertRaises(ValueError): kb.sources(['nist-msa'],context=self.context,packs=['backend'])
        qa=kb.available('quality-assurance',limit=1)['personas'][0]['context']
        with self.assertRaises(ValueError): kb.read(['backend:pool-exhaustion'],context=qa)
        with self.assertRaises(ValueError): kb.sources(['backend-lab'],context=qa)
    def test_empty_and_missing_context(self):
        self.assertEqual(kb.lookup('zznonesuch987654',context=self.context,limit=2,max_chars=1800)['matches'],[])
        with self.assertRaises(ValueError): kb.lookup('pool',context='backend-expert')
    def test_mcp_same_limits(self):
        result=dispatch({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'expert_lookup','arguments':{
            'query':'DB 연결 풀 고갈','context':self.context,'limit':2,'max_chars':1800}}},{'ready':True})
        self.assertFalse(result['result']['isError'])
        text=result['result']['content'][0]['text']
        self.assertLessEqual(len(text),1800)
        self.assertIn('backend:pool-exhaustion',[r['id'] for r in json.loads(text)['matches']])
    def test_cli_context_and_data_comparison(self):
        command=[sys.executable,'-B','-X','utf8',str(SKILL/'scripts/expert.py')]
        run=subprocess.run(command+['lookup','DB 연결 풀 고갈','--context',self.context,'--limit','2','--max-chars','1800'],capture_output=True,text=True,encoding='utf-8',check=True)
        self.assertIn('backend:pool-exhaustion',[r['id'] for r in json.loads(run.stdout)['matches']])
        helper=SKILL/'scripts/compare_backend_runs.py'
        ev=SKILL/'evidence/backend-lab/lab-20261029'
        run=subprocess.run([sys.executable,str(helper),str(ev/'before-1.json'),str(ev/'after-1.json')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertTrue(json.loads(run.stdout))

if __name__=='__main__': unittest.main(verbosity=2)
