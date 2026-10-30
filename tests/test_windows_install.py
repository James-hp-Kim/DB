"""Check installation with isolated Codex config; output path must be new."""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--out',type=Path,required=True)
    target=parser.parse_args().out.resolve(); target.mkdir(parents=True,exist_ok=False)
    codex=shutil.which('codex.cmd') or shutil.which('codex')
    if not codex: raise SystemExit('Codex CLI required')
    env=os.environ.copy(); env['PYTHONUTF8']='1'; env['PYTHONDONTWRITEBYTECODE']='1'; env['EXPERT_CONTEXT_DIR']=str(target/'contexts')
    env['CODEX_HOME']=str(target/'isolated-skill'); Path(env['CODEX_HOME']).mkdir()
    results=[]
    def run(name,args,expected=0):
        p=subprocess.run(args,cwd=BASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        (target/(name+'.log')).write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
        results.append({'test':name,'passed':p.returncode==expected})
        if p.returncode!=expected: raise RuntimeError(name+' failed; see '+str(target))
        return p
    ps=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File']
    run('environment',ps+[str(BASE/'Test-Environment.ps1')])
    dest=target/'공백 포함'/'expert'
    run('skill-mcp',ps+[str(BASE/'Install.ps1'),'-SkillDestination',str(dest),'-EnableMcp'])
    run('no-overwrite',ps+[str(BASE/'Install.ps1'),'-SkillDestination',str(dest)],1)
    run('mcp-list',[codex,'mcp','list','--json'])
    env['CODEX_HOME']=str(target/'isolated-plugin'); Path(env['CODEX_HOME']).mkdir()
    run('plugin-install',ps+[str(BASE/'Install.ps1'),'-Mode','Plugin'])
    listing=json.loads(run('plugin-list',[codex,'plugin','list','--json']).stdout)
    assert any(p['pluginId']=='expert-hub@expert-local' and p['installed'] and p['enabled'] for p in listing['installed'])
    choices=json.loads(run('wrapper-personas',ps+[str(BASE/'expert.ps1'),'catalog','품질보증','--limit','1']).stdout)
    context=choices['personas'][0]['context']
    run('wrapper-search',ps+[str(BASE/'expert.ps1'),'lookup','불량률 분모','--context',context])
    run('wrapper-missing-context',ps+[str(BASE/'expert.ps1'),'lookup','불량률 분모'],2)
    print(json.dumps({'passed':True,'checks':results},ensure_ascii=False,indent=2))


if __name__=='__main__': main()
