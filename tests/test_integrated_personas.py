"""Integration coverage for every persona and the shared chip input router."""
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

class IntegratedPersonas(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='통합 전문가 ')
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':self.tmp.name});self.env.start()
    def tearDown(self): self.env.stop();self.tmp.cleanup()

    def test_every_persona_bounded_roundtrip(self):
        for pid,profile in kb.catalog().items():
            with self.subTest(persona=pid):
                selected=kb.available(pid,limit=1)['personas'][0]
                self.assertEqual(selected['id'],pid)
                context=selected['context'];pack=profile['default_packs'][0]
                # Maintenance fixture reads one canonical title; clients use lookup results.
                row=json.loads((SKILL/f'packs/{pack}/records.jsonl').read_text(encoding='utf-8').splitlines()[0])
                found=kb.lookup(row['title'],context=context,limit=2,max_chars=2000)
                self.assertTrue(found['matches'])
                self.assertLessEqual(len(dump(found)),2000)
                rid=found['matches'][0]['id']
                read=kb.read([rid],context=context,sections=['conditions','limits'],max_chars=3000)
                self.assertLessEqual(len(dump(read)),3000)
                self.assertTrue(kb.sources([read['items'][0]['sources'][0]],context=context)['sources'])

    def test_semiconductor_ai_routes_supplied_files(self):
        context=kb.available('semiconductor-ai',limit=1)['personas'][0]['context']
        fixtures=[('timing.rpt','WNS -0.1 setup hold secret-marker','chip-rtl'),
                  ('memory.txt','refresh tREFI tRFC secret-marker','chip-memory'),
                  ('circuit.sp','* SPICE noise corner secret-marker','chip-analog'),
                  ('review.txt','secret-marker','chip-review')]
        for name,text,expected in fixtures:
            with self.subTest(name=name):
                p=Path(self.tmp.name)/name;p.write_text(text,encoding='utf-8')
                result=reference_input(p,context=context,query='검토 근거' if expected=='chip-review' else None)
                self.assertEqual(result['selected_pack'],expected)
                self.assertNotIn('secret-marker',dump(result))
                self.assertLessEqual(len(dump(result)),3500)
                self.assertTrue(all(x['id'].startswith(expected+':') for x in result.get('retrieval',{}).get('matches',[])))

if __name__=='__main__':unittest.main(verbosity=2)
