"""Policy delivery, fallback and selective knowledge additions; no external servers."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
SKILL = BASE / 'plugins/expert-hub/skills/expert'
sys.path.insert(0, str(SKILL / 'scripts'))
import knowledge as kb
from grounding import policy
from qa_core import dump


class GroundingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {'EXPERT_CONTEXT_DIR':str(self.home/'contexts'), 'CODEX_HOME':str(self.home/'codex')})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_installed_policy_has_priority_and_detects_updates(self):
        path = self.home/'codex/skills/fact-grounding/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('현재 정책 테스트', encoding='utf-8')
        first = policy(SKILL)
        self.assertEqual(first['origin'], 'installed-skill')
        self.assertEqual(first['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        path.write_text('업데이트된 정책 테스트', encoding='utf-8')
        self.assertNotEqual(first['sha256'], policy(SKILL)['sha256'])

    def test_fallback_and_missing_guide_are_honest(self):
        result = policy(SKILL)
        self.assertEqual(result['origin'], 'bundled-snapshot')
        self.assertTrue(Path(result['guide']).is_file())
        self.assertNotIn('applied', result)
        self.assertIn('not proof', result['enforcement'])
        with self.assertRaises(FileNotFoundError):
            policy(self.home/'empty')

    def test_all_personas_receive_policy_with_scoped_evidence(self):
        for pid, profile in kb.catalog().items():
            with self.subTest(persona=pid):
                selection = kb.available(pid, limit=1)
                self.assertEqual(selection['fact_grounding']['skill'], 'fact-grounding')
                self.assertEqual(selection['personas'][0]['id'], pid)
                ctx = selection['personas'][0]['context']
                result = kb.lookup('요구사항 검증', context=ctx, max_chars=1200)
                self.assertIn('fact-grounding', result['fact_grounding'])
                self.assertLessEqual(len(dump(result)),1200)
                hit = kb.lookup('요구사항과 검증 증거 연결', context=ctx, packs=['common'])
                self.assertIn('common:requirements-to-evidence', [x['id'] for x in hit['matches']])
                row = kb.read(['common:requirements-to-evidence'], context=ctx, packs=['common'], sections=['limits'])['items'][0]
                self.assertTrue(kb.sources([row['sources'][0]], context=ctx, packs=['common'])['sources'])

    def test_new_backend_guidance_retrieves_and_remains_scoped(self):
        ctx = kb.available('backend-expert',limit=1)['personas'][0]['context']
        for query,rid in [('버그 최소 재현','backend:minimal-reproduction'),('동작 보존 리팩터링','backend:behavior-preserving-refactor')]:
            self.assertIn(rid,[x['id'] for x in kb.lookup(query,context=ctx)['matches']])
        qa = kb.available('quality-assurance',limit=1)['personas'][0]['context']
        with self.assertRaises(ValueError):kb.read(['backend:minimal-reproduction'],context=qa)

    def test_real_stdio_delivers_policy_for_every_persona(self):
        requests = [{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25'}},
                    {'jsonrpc':'2.0','method':'notifications/initialized'}]
        for i,pid in enumerate(kb.catalog(),2):
            requests.append({'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':'expert_catalog','arguments':{'query':pid,'limit':1}}})
        completed = subprocess.run([sys.executable,'-B','-X','utf8',str(SKILL/'scripts/mcp_server.py')],input='\n'.join(map(json.dumps,requests))+'\n',encoding='utf-8',capture_output=True,timeout=30,check=True)
        responses=[json.loads(line) for line in completed.stdout.splitlines()]
        self.assertEqual(len(responses),1+len(kb.catalog()))
        self.assertIn('fact-grounding', responses[0]['result']['instructions'])
        for response,pid in zip(responses[1:],kb.catalog()):
            result=response['result'];self.assertFalse(result['isError'])
            data=json.loads(result['content'][0]['text'])
            self.assertEqual(data['personas'][0]['id'],pid)
            self.assertEqual(data['fact_grounding']['skill'],'fact-grounding')


if __name__ == '__main__':unittest.main(verbosity=2)
