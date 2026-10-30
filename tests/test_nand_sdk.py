"""Optional official SDK check for NAND lookup and file reference."""
import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    base=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='nand-sdk-') as temp:
        params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(base/'plugins/expert-hub/skills/expert/scripts/mcp_server.py')],env={**os.environ,'EXPERT_CONTEXT_DIR':temp})
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                init=await session.initialize()
                choice=await session.call_tool('expert_catalog',{'query':'NAND','limit':1})
                persona=json.loads(choice.content[0].text)['personas'][0]
                assert persona['id']=='nand-expert'
                ctx=persona['context']
                found=await session.call_tool('expert_lookup',{'query':'P01','context':ctx})
                assert json.loads(found.content[0].text)['matches'][0]['id']=='nand:p01'
                detail=await session.call_tool('expert_read',{'ids':['nand:p14'],'sections':['limits'],'context':ctx})
                assert json.loads(detail.content[0].text)['items'][0]['evidence']=='program_only'
                src=await session.call_tool('expert_source',{'ids':['nand-p01'],'context':ctx})
                assert 'arxiv.org' in json.loads(src.content[0].text)['sources'][0]['url']
                routed=await session.call_tool('expert_reference_input',{'file':str(base/'examples/nand-retry-synthetic.log'),'context':ctx,'max_chars':2400})
                assert not routed.isError
                result=json.loads(routed.content[0].text)
                assert 'nand:v12' in [x['id'] for x in result['retrieval']['matches']]
                print(json.dumps({'passed':True,'protocol':init.protocolVersion,'persona':'nand-expert','lookup_read_source':'PASS','file_reference':'PASS'},ensure_ascii=False))

if __name__=='__main__':asyncio.run(asyncio.wait_for(main(),timeout=30))
