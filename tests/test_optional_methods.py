import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'plugins/expert-hub/skills/expert/scripts'))
import knowledge as kb
import optional_methods as methods


class OptionalMethodTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.env=patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':self.temp.name})
        self.env.start()
        self.context=kb.available('backend-expert',limit=1)['personas'][0]['context']

    def tearDown(self):
        self.env.stop();self.temp.cleanup()

    def test_catalog_is_bounded_and_no_procedures(self):
        rows=methods.choices()
        self.assertEqual(len(rows),10)
        self.assertTrue(all('steps' not in x and 'dependencies' not in x for x in rows))

    def test_all_methods_require_approval(self):
        for name in methods.catalog():
            for approval in (False,None,'true',1):
                with self.subTest(name=name,approval=approval), self.assertRaises(ValueError):
                    methods.read(name,self.context,approved=approval,complex_problem=True)

    def test_complex_wording_alone_is_not_consent(self):
        with self.assertRaises(ValueError):methods.read('grilling',self.context,complex_problem=True)
        with self.assertRaises(ValueError):methods.read('grilling',self.context,approved=True)
        with self.assertRaises(ValueError):methods.read('grilling',self.context,approved=True,complex_problem='true')
        self.assertTrue(methods.read('grilling',self.context,True,True)['steps'])

    def test_alias_resolves_once_and_all_guides_open_after_consent(self):
        for name in methods.catalog():
            self.assertTrue(methods.read(name,self.context,True,True)['steps'])
        self.assertEqual(methods.read('grill-me',self.context,True,True)['name'],'grilling')

    def test_persona_gate_and_unknown_name(self):
        with self.assertRaises(ValueError):methods.read('caveman','f'*24,True)
        with self.assertRaises(ValueError):methods.read('../SKILL.md',self.context,True)

    def test_every_persona_can_read_approved_shared_method(self):
        for pid in kb.catalog():
            ctx=kb.available(pid,limit=1)['personas'][0]['context']
            self.assertEqual(methods.read('ponytail',ctx,True)['name'],'ponytail')


if __name__=='__main__':unittest.main()
