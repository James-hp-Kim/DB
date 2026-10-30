"""Real stdio MCP interoperability for the HBM workflow, using the official SDK."""
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    base=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='HBM MCP 한글 ') as tmp:
        params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(base/'plugins/expert-hub/skills/expert/scripts/mcp_server.py')],env={**os.environ,'EXPERT_CONTEXT_DIR':tmp})
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                initialized=await session.initialize()
                async def call(name,arguments):
                    result=await session.call_tool(name,arguments)
                    assert not result.isError, result
                    return json.loads(result.content[0].text)
                choice=await call('expert_catalog',{'query':'hbm-expert','limit':1})
                context=choice['personas'][0]['context']
                routed=await call('expert_reference_input',{'file':str(base/'examples/hbm-warpage-synthetic.txt'),'context':context,'query':'warpage','max_chars':2500})
                assert routed['retrieval']['packs']==['hbm']
                assert 'hbm:paper-a23' in [x['id'] for x in routed['retrieval']['matches']]
                found=await call('expert_lookup',{'query':'14도','context':context,'limit':2,'max_chars':2000})
                assert 'hbm:correction-r09' in [x['id'] for x in found['matches']]
                page=await call('expert_read',{'ids':['hbm:paper-p01'],'sections':['conditions','interpretation','limits'],'context':context,'max_chars':3000})
                assert all(x['next_offset'] is None for x in page['items'])
                source=await call('expert_source',{'ids':page['items'][0]['sources'],'context':context,'max_chars':3000})
                assert source['sources'] and not source['omitted_ids']
                rejected=await session.call_tool('expert_read',{'ids':['nand:p01'],'context':context})
                assert rejected.isError
                print(json.dumps({'passed':True,'protocol':initialized.protocolVersion,'workflow':['catalog','reference_input','lookup','read','source'],'foreign_pack_rejected':True,'app_activation_tested':False},ensure_ascii=False))

if __name__=='__main__':asyncio.run(main())
