"""Retrieval and input-routing checks, not semiconductor diagnosis accuracy."""
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from input_reference import reference_input
from qa_core import dump


class SemiconductorAI(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='반도체 AI 검증 ')
        self.path=Path(self.tmp.name)
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':str(self.path/'contexts')})
        self.env.start()
        self.context=kb.available('semiconductor-ai',limit=1)['personas'][0]['context']

    def tearDown(self):
        self.env.stop();self.tmp.cleanup()

    def test_persona_and_default_scope(self):
        self.assertEqual(kb.available('반도체 AI 스킬 전문가',limit=1)['personas'][0]['id'],'semiconductor-ai')
        r=kb.lookup('설계 개선',context=self.context)
        self.assertTrue(all(x['id'].startswith('chip-review:') for x in r['matches']))
        with self.assertRaises(ValueError):kb.lookup('x',context=self.context,packs=['backend'])
        with self.assertRaises(ValueError):kb.lookup('x',packs=['chip-rtl'])

    def test_relevant_top_three(self):
        cases=[('hold slack','chip-rtl','claim-c06'),('multicycle','chip-rtl','claim-c05'),
               ('barrel','chip-rtl','config-barrel'),('DRAM','chip-memory','model-levels'),
               ('noise','chip-analog','claim-c34')]
        for q,p,rid in cases:
            with self.subTest(query=q):
                r=kb.lookup(q,context=self.context,packs=[p],limit=3)
                self.assertIn(p+':'+rid,[x['id'] for x in r['matches']])

    def test_all_added_records_have_conditions_limits_and_resolvable_sources(self):
        sources=json.loads((SKILL/'knowledge/sources.json').read_text(encoding='utf-8'))
        n=0
        for p in (SKILL/'packs').glob('chip-*/records.jsonl'):
            for line in p.read_text(encoding='utf-8').splitlines():
                r=json.loads(line);n+=1
                self.assertTrue(r['sections']['conditions'],r['id'])
                self.assertTrue(r['sections']['limits'],r['id'])
                self.assertTrue(all(s in sources for s in r['source_ids']))
        self.assertEqual(n,102)

    def test_input_routing_no_raw_content_or_mutation(self):
        for name,body,expected in [('설계.sv','module m; always_ff @(posedge clk) q<=d; endmodule','chip-rtl'),
                                   ('조건.sdc','set_multicycle_path 2 -setup','chip-rtl'),
                                   ('메모리.log','tREFI refresh tRFC','chip-memory'),
                                   ('아날로그.sp','V1 in 0 1\n.op\n.end','chip-analog')]:
            with self.subTest(name=name):
                f=self.path/name;f.write_text('PRIVATE_CANARY_028\n'+body,encoding='utf-8')
                before=hashlib.sha256(f.read_bytes()).hexdigest()
                r=reference_input(f,context=self.context,max_chars=2500)
                self.assertEqual(r['selected_pack'],expected)
                self.assertLessEqual(len(dump(r)),2500)
                self.assertNotIn('PRIVATE_CANARY',dump(r))
                self.assertEqual(before,hashlib.sha256(f.read_bytes()).hexdigest())
                self.assertTrue(all(x['id'].startswith(expected+':') for x in r['retrieval']['matches']))

    def test_caps_and_section_selection(self):
        for cap in [1200,2000,3500]:
            r=kb.lookup('hold slack STA',context=self.context,packs=['chip-rtl'],limit=8,max_chars=cap)
            self.assertLessEqual(len(dump(r)),cap)
        r=kb.read(['chip-rtl:claim-c06'],context=self.context,packs=['chip-rtl'],sections=['conditions','limits'],max_chars=2400)
        self.assertLessEqual(len(dump(r)),2400)
        self.assertEqual({x['section'] for x in r['items']},{'conditions','limits'})

    def test_missing_context_before_open_and_unsupported_file(self):
        with patch.object(Path,'stat',side_effect=AssertionError('file access before gate')):
            with self.assertRaises(ValueError):reference_input('absent.sv')
        with self.assertRaises(ValueError):reference_input(self.path/'x.pdf',context=self.context)
        f=self.path/'unknown.txt';f.write_text('abcdefzzz',encoding='utf-8')
        self.assertIn('gap',reference_input(f,context=self.context))

    def test_sources_and_archive_integrity(self):
        r=kb.sources(['chip-public-experiment'],context=self.context,packs=['chip-rtl'])
        self.assertTrue(r['sources'][0]['url'])
        expected=json.loads((BASE/'docs/semiconductor-import.json').read_text(encoding='utf-8'))['archive_sha256']
        self.assertEqual(hashlib.sha256((BASE/'third_party/semiconductor-evidence-20261029.zip').read_bytes()).hexdigest(),expected)

if __name__=='__main__':unittest.main(verbosity=2)
