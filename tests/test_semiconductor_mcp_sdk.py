"""Optional official MCP SDK test for the semiconductor path over real stdio."""
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def error(response):
    return getattr(response, 'isError', getattr(response, 'is_error', False))


async def main():
    root=Path(__file__).resolve().parents[1]
    script=root/'plugins/expert-hub/skills/expert/scripts/mcp_server.py'
    with tempfile.TemporaryDirectory(prefix='반도체 MCP ') as temp:
        params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(script)],
            env={**os.environ,'EXPERT_CONTEXT_DIR':temp})
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                init=await session.initialize()
                listing=await session.list_tools()
                names={t.name for t in listing.tools}
                assert {'expert_catalog','expert_lookup','expert_read','expert_source'} <= names
                response=await session.call_tool('expert_catalog',{'query':'반도체기초전문가','limit':1})
                choice=json.loads(response.content[0].text)['personas'][0]
                assert choice['id']=='semiconductor-basics'
                ctx=choice['context']
                response=await session.call_tool('expert_lookup',{'query':'단일 소자 누설 분해','context':ctx,'max_chars':2500})
                assert not error(response)
                assert 'semiconductor:e01' in [r['id'] for r in json.loads(response.content[0].text)['matches']]
                response=await session.call_tool('expert_read',{'ids':['semiconductor:e01'],'sections':['conditions','limits'],'context':ctx})
                assert not error(response) and '미실행' in response.content[0].text
                sid=json.loads(response.content[0].text)['items'][0]['sources'][0]
                response=await session.call_tool('expert_source',{'ids':[sid],'context':ctx})
                assert not error(response) and json.loads(response.content[0].text)['sources'][0]['url']
                response=await session.call_tool('expert_read',{'ids':['quality:msa'],'context':ctx})
                assert error(response)
                print(json.dumps({'passed':True,'protocol':getattr(init,'protocolVersion',getattr(init,'protocol_version',None)),'tools':sorted(names),
                                  'scope_rejection':True,'catalog_lookup_read_source':True},ensure_ascii=False))


if __name__=='__main__': asyncio.run(main())
