"""Isolated new installation: no existing Skills/MCP/plugins; host Python/CLI reused."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

BASE=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();target=args.out.resolve();target.mkdir(parents=True,exist_ok=False)
    dest=target/'새 PC 공백 경로'/'expert';codex_home=target/'empty-codex';codex_home.mkdir()
    env=dict(os.environ,CODEX_HOME=str(codex_home),EXPERT_CONTEXT_DIR=str(target/'contexts'),PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
    codex=shutil.which('codex.cmd') or shutil.which('codex')
    if not codex:raise SystemExit('Codex CLI needed for isolated registration test')
    tests=[]
    def run(name,cmd,code=0):
        p=subprocess.run(cmd,cwd=BASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        tests.append({'name':name,'exit_code':p.returncode,'passed':p.returncode==code})
        (target/(name+'.log')).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
        if p.returncode!=code:raise RuntimeError(name+' failed')
        return p
    before=run('empty-mcp',[codex,'mcp','list','--json'])
    assert json.loads(before.stdout)==[]
    cmd=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(BASE/'Setup-NewPC.ps1'),'-PythonExe',sys.executable,'-SkillDestination',str(dest)]
    run('setup',cmd)
    installed=json.loads(run('registered-mcp',[codex,'mcp','list','--json']).stdout)
    assert len(installed)==1 and installed[0]['name']=='expert-knowledge'
    assert not (codex_home/'skills').exists()
    out=target/'persona-results.json'
    run('fresh-connection',[sys.executable,'-B','-X','utf8',str(dest/'scripts/verify_install.py'),'--out',str(out)])
    checks=json.loads(out.read_text(encoding='utf-8'))
    assert len(checks['personas'])==9 and all(x['grounding_origin']=='bundled-snapshot' for x in checks['personas'])
    run('preserve-existing',cmd,1)
    manual=target/'manual-install'
    run('manual-setup',['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(BASE/'Setup-NewPC.ps1'),'-PythonExe',sys.executable,'-SkillDestination',str(manual),'-ManualMcp'])
    after=json.loads(run('manual-no-extra-registration',[codex,'mcp','list','--json']).stdout)
    assert after==installed
    report={'passed':True,'checks':tests,'fallback_personas':9,'new_connection_version':checks['server_version'],'limits':'Same Windows PC with isolated configuration and new install paths. Host Python and Codex CLI reused; no clean OS or other physical computer tested.'}
    (target/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
