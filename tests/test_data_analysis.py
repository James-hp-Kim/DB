import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from profile_data import profile
from qa_core import dump,digest

class DataAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':str(self.path/'contexts')});self.env.start()
        self.context=kb.available('빅데이터',limit=1)['personas'][0]['context']
    def tearDown(self):self.env.stop();self.tmp.cleanup()
    def test_role_and_scope(self):
        self.assertEqual(kb.available('빅데이터',limit=1)['personas'][0]['id'],'data-analyst')
        self.assertEqual(kb.scope(self.context)[0]['default_packs'],['common','analytics'])
        with self.assertRaises(ValueError):kb.read(['sales:backtest'],context=self.context)
        with self.assertRaises(ValueError):kb.lookup('x',context=self.context,packs=['nand'])
    def test_expected_retrieval(self):
        for query,pack,rid in [('백테스트','sales','sales:backtest'),('WAPE 분모','sales','sales:metrics'),('Optuna pruning','analytics','analytics:hpo'),('대용량 메모리 스트리밍','analytics','analytics:large-data'),('딥러닝 GPU','analytics','analytics:deep-learning')]:
            result=kb.lookup(query,context=self.context,packs=[pack],max_chars=2500)
            self.assertIn(rid,[x['id'] for x in result['matches']],query)
            self.assertLessEqual(len(dump(result)),2500)
    def test_conditions_limits_sources(self):
        part=kb.read(['sales:backtest'],context=self.context,packs=['sales'],max_chars=2500)
        self.assertEqual({p['section'] for p in part['items']},{'conditions','procedure','limits'})
        self.assertTrue(all(p['text'] for p in part['items']))
        self.assertTrue(kb.sources(['da-fpp'],context=self.context,packs=['sales'])['sources'])
    def test_all_new_records_resolve(self):
        for pack,expected in [('analytics',10),('sales',14)]:
            records=[json.loads(l) for l in (SKILL/f'packs/{pack}/records.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(records),expected)
            for r in records:
                self.assertIn('limits',r['sections']);self.assertIn('conditions',r['sections'])
                self.assertTrue(kb.sources(r['source_ids'],context=self.context,packs=[pack])['sources'])
    def test_full_profile_and_source_preserved(self):
        file=SKILL/'examples/synthetic-monthly.csv'; before=digest(file)
        p=profile(file,columns=['unique_id','ds','y'],date_column='ds',task='forecast')
        self.assertEqual(p['rows_scanned'],360);self.assertTrue(p['complete_scan'])
        self.assertEqual(p['columns'][0]['distinct_at_least'],3)
        self.assertEqual(p['dates']['valid'],360)
        self.assertEqual(digest(file),before);self.assertNotIn('001',dump(p))
    def test_prefix_and_cardinality_bound(self):
        file=self.path/'many.csv'
        with file.open('w',newline='',encoding='utf-8') as s:
            w=csv.writer(s);w.writerow(['id']);w.writerows([[f'secret-{i}'] for i in range(1000)])
        p=profile(file,max_rows=300)
        self.assertEqual(p['rows_scanned'],300);self.assertFalse(p['complete_scan'])
        self.assertTrue(p['columns'][0]['distinct_capped']);self.assertEqual(p['columns'][0]['distinct_at_least'],257)
        self.assertNotIn('secret-',dump(p))
        self.assertTrue(profile(file,max_rows=1000)['complete_scan'])
    def test_invalid_input(self):
        file=self.path/'bad.csv'
        for text in ['x,x\n1,2\n','x,y\n1\n','']:
            file.write_text(text,encoding='utf-8')
            with self.assertRaises(ValueError):profile(file)
        file.write_text('x\n1\n',encoding='utf-8')
        with self.assertRaises(ValueError):profile(file,max_rows=-1)
        with self.assertRaises(ValueError):profile(file,date_column='missing')
    def test_null_nonfinite_date_and_budget(self):
        file=self.path/'values.csv';file.write_text('date,value\n2020-01-01,0\nnot-date,nan\n2020-02-01,-5\n,\n',encoding='utf-8')
        p=profile(file,date_column='date',max_chars=1500)
        self.assertLessEqual(len(dump(p)),1500)
        self.assertEqual(p['dates']['invalid'],1);self.assertEqual(p['dates']['valid'],2)
        full=profile(file,date_column='date')
        s=full['columns'][1];self.assertEqual((s['nonfinite'],s['missing'],s['negative'],s['zero']),(1,1,1,1))
    def test_cli_profile(self):
        p=subprocess.run([sys.executable,'-B','-X','utf8',str(SKILL/'scripts/expert.py'),'profile',str(SKILL/'examples/synthetic-monthly.csv'),'--task','forecast'],capture_output=True,text=True,encoding='utf-8',check=True)
        self.assertEqual(json.loads(p.stdout)['suggested_lookups'][1]['packs'],['sales'])

if __name__=='__main__':unittest.main()
