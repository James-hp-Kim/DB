"""Start a fresh MCP connection and verify each persona without an MCP SDK."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]


def verify():
    with tempfile.TemporaryDirectory(prefix='expert-check-') as temp:
        env = dict(os.environ, EXPERT_CONTEXT_DIR=str(Path(temp)/'contexts'))
        process = subprocess.Popen([sys.executable,'-B','-X','utf8',str(ROOT/'scripts/mcp_server.py')],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
            text=True,encoding='utf-8',env=env)
        responses = queue.Queue()
        def receive():
            for line in process.stdout:responses.put(line)
            responses.put(None)
        threading.Thread(target=receive,daemon=True).start()
        counter = 0
        def send(method, params=None, notification=False):
            nonlocal counter
            request={'jsonrpc':'2.0','method':method}
            if params is not None:request['params']=params
            if not notification:
                counter+=1;request['id']=counter
            process.stdin.write(json.dumps(request)+'\n');process.stdin.flush()
            if notification:return
            line=responses.get(timeout=20)
            if line is None:raise RuntimeError('MCP server closed before responding')
            response=json.loads(line)
            if response.get('id')!=counter or 'error' in response:raise RuntimeError('Invalid MCP response')
            return response['result']
        def call(name, args):
            result=send('tools/call',{'name':name,'arguments':args})
            if result.get('isError'):raise RuntimeError(result['content'][0]['text'])
            return json.loads(result['content'][0]['text'])
        try:
            init=send('initialize',{'protocolVersion':'2025-11-25','clientInfo':{'name':'expert-install-check','version':'1'},'capabilities':{}})
            send('notifications/initialized',notification=True)
            assert 'fact-grounding' in init['instructions']
            tools=send('tools/list')['tools']
            assert len(tools)==5
            personas=json.loads((ROOT/'personas/catalog.json').read_text(encoding='utf-8'))
            rows=[]
            for pid in personas:
                selected=call('expert_catalog',{'query':pid,'limit':1})
                entry=selected['personas'][0];assert entry['id']==pid
                policy=selected['fact_grounding'];guide=Path(policy['guide'])
                guide_bytes=guide.read_bytes()
                assert hashlib.sha256(guide_bytes).hexdigest()==policy['sha256']
                assert '사실' in guide_bytes.decode('utf-8-sig')
                assert policy['optional_methods'].startswith('Default off')
                ctx=entry['context']
                found=call('expert_lookup',{'query':'선택 기능의 동의와 조회량 제한','context':ctx,'packs':['common'],'limit':1,'max_chars':1500})
                rid='common:optional-method-consent'
                assert found['matches'][0]['id']==rid
                new=call('expert_read',{'ids':[rid,'common:requirements-to-evidence'],'context':ctx,'packs':['common'],'sections':['conditions','limits'],'max_chars':3000})
                assert {x['id'] for x in new['items']}=={rid,'common:requirements-to-evidence'}
                source_ids=list(dict.fromkeys(s for x in new['items'] for s in x['sources']))[:5]
                evidence=call('expert_source',{'ids':source_ids,'context':ctx,'packs':['common'],'max_chars':5000})
                assert evidence['sources']
                rows.append({'persona':pid,'passed':True,'grounding_origin':policy['origin'],'guide_hash_match':True,'new_record':rid,'previous_addition':'common:requirements-to-evidence','source_count':len(evidence['sources'])})
            return {'passed':True,'server_version':init['serverInfo']['version'],'protocol':init['protocolVersion'],'tools':len(tools),'personas':rows,
                'limits':'Fresh stdio connection and policy/evidence delivery tested. Not a desktop reconnect or model-compliance evaluation.'}
        finally:
            process.stdin.close()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)
            process.stdout.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    try:result=verify()
    except (AssertionError,ValueError,KeyError,OSError,RuntimeError,queue.Empty) as exc:
        result={'passed':False,'error':str(exc) or type(exc).__name__}
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.out:args.out.write_text(text+'\n',encoding='utf-8')
    print(text)
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
