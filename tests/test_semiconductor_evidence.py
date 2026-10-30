"""Relevant HBM scope works through the shared gate without widening other roles."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL=Path(__file__).resolve().parents[1]/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from mcp_server import dispatch

class SemiconductorEvidenceTests(unittest.TestCase):
    def test_ai_hbm_lookup_read_source_and_scope_preserved(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':tmp}):
            selected=kb.available('semiconductor-ai',limit=1)['personas'][0]
            self.assertIn('hbm',selected['allowed_packs'])
            key=selected['context']
            hits=kb.lookup('thermal',context=key,packs=['hbm'])['matches']
            self.assertTrue(hits)
            record=hits[0]
            parts=kb.read([record['id']],context=key,packs=['hbm'],sections=['conditions','limits'])['items']
            self.assertTrue(any(p['present'] and p['text'] for p in parts))
            sid=parts[0]['sources'][0]
            self.assertEqual(kb.sources([sid],context=key,packs=['hbm'])['sources'][0]['id'],sid)
            with self.assertRaises(ValueError): kb.read([record['id']],context=key)
            with self.assertRaises(ValueError): kb.sources([record['id']],context=key,packs=['hbm'])
            response=dispatch({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'expert_source','arguments':{'context':key,'packs':['hbm'],'ids':[sid]}}},{'ready':True})
            self.assertFalse(response['result']['isError'])

    def test_unrelated_persona_still_cannot_read_hbm(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':tmp}):
            key=kb.available('backend-expert',limit=1)['personas'][0]['context']
            with self.assertRaises(ValueError): kb.lookup('thermal',context=key,packs=['hbm'])

if __name__=='__main__':unittest.main()
