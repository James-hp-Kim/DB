"""Windows relocation, Skill copy and PowerShell flow without user configuration edits."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name=='nt','Windows PowerShell test')
class WindowsChipFlow(unittest.TestCase):
    def test_isolated_install_no_overwrite_and_bounded_flow(self):
        with tempfile.TemporaryDirectory(prefix='칩 설치 공백 ') as temp:
            target=Path(temp)/'test-skill'
            env={**os.environ,'PATH':str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH',''),
                 'EXPERT_CONTEXT_DIR':str(Path(temp)/'contexts'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
            prefix=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File']
            def run(args, code=0):
                result=subprocess.run(args,cwd=BASE,env=env,capture_output=True,encoding='utf-8',timeout=45)
                self.assertEqual(result.returncode,code,result.stderr)
                return result.stdout
            run(prefix+[str(BASE/'Install.ps1'),'-SkillDestination',str(target),'-PythonExe',sys.executable])
            run(prefix+[str(BASE/'Install.ps1'),'-SkillDestination',str(target),'-PythonExe',sys.executable],1)
            cli=[sys.executable,'-B','-X','utf8',str(target/'scripts/expert.py')]
            choice=json.loads(run(cli+['catalog','chip-design-verification','--limit','1']))
            context=choice['personas'][0]['context']
            result=json.loads(run(cli+['reference-input',str(BASE/'examples/chip-timing-synthetic.rpt'),'--context',context,'--max-chars','2500']))
            self.assertIn('rtl:c22',[x['id'] for x in result['retrieval']['matches']])
            wrapper=prefix+[str(BASE/'expert.ps1')]
            # Receipts cannot cross installation roots. Obtain a new one for the repository wrapper.
            run(wrapper+['lookup','WNS','--context',context],2)
            choice=json.loads(run(wrapper+['catalog','chip-design-verification','--limit','1']))
            context=choice['personas'][0]['context']
            result=json.loads(run(wrapper+['reference-input',str(BASE/'examples/chip-timing-synthetic.rpt'),'--context',context]))
            self.assertEqual(result['persona'],'chip-design-verification')
            run(wrapper+['lookup','WNS'],2)


if __name__=='__main__':unittest.main(verbosity=2)
