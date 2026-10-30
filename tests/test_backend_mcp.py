"""Official SDK stdio interoperability for the backend persona, including source scope."""
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    root=Path(__file__).resolve().parents[1]/'plugins/expert-hub/skills/expert'
    with tempfile.TemporaryDirectory(prefix='backend-mcp-') as temporary:
        params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(root/'scripts/mcp_server.py')],
            env={**os.environ,'EXPERT_CONTEXT_DIR':temporary})
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                initialized=await session.initialize()
                choices=await session.call_tool('expert_catalog',{'query':'백엔드','limit':1})
                selected=json.loads(choices.content[0].text)['personas'][0]
                assert selected['id']=='backend-expert'
                context=selected['context']
                result=await session.call_tool('expert_lookup',{'query':'DB 연결 풀 고갈','context':context,'limit':2,'max_chars':1800})
                assert not result.isError
                text=result.content[0].text
                assert len(text)<=1800
                assert 'backend:pool-exhaustion' in [r['id'] for r in json.loads(text)['matches']]
                result=await session.call_tool('expert_read',{'ids':['backend:pool-exhaustion'],'context':context,'sections':['conditions','procedure','limits'],'max_chars':3000})
                assert not result.isError and len(result.content[0].text)<=3000
                assert all(r['next_offset'] is None for r in json.loads(result.content[0].text)['items'])
                result=await session.call_tool('expert_source',{'ids':['backend-lab'],'context':context,'max_chars':2000})
                assert not result.isError and 'measured-synthetic' in result.content[0].text
                denied=await session.call_tool('expert_read',{'ids':['quality:msa'],'context':context})
                assert denied.isError
                print(json.dumps({'passed':True,'protocol':initialized.protocolVersion,
                  'checks':['persona-search','bounded-lookup','selected-sections','source','out-of-scope-denial']},ensure_ascii=False))

if __name__=='__main__': asyncio.run(main())
