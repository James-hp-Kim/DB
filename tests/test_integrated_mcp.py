"""Official SDK check for the shared semiconductor-ai file routing branch."""
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    base=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='통합 MCP ') as tmp:
        path=Path(tmp)/'timing.rpt';path.write_text('WNS -0.1 setup hold secret-marker',encoding='utf-8')
        params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(base/'plugins/expert-hub/skills/expert/scripts/mcp_server.py')],env={**os.environ,'EXPERT_CONTEXT_DIR':str(Path(tmp)/'contexts')})
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                init=await session.initialize()
                selected=await session.call_tool('expert_catalog',{'query':'semiconductor-ai','limit':1})
                context=json.loads(selected.content[0].text)['personas'][0]['context']
                response=await session.call_tool('expert_reference_input',{'file':str(path),'context':context})
                assert not response.isError,response
                text=response.content[0].text;result=json.loads(text)
                assert result['selected_pack']=='chip-rtl'
                assert result['retrieval']['matches']
                assert 'secret-marker' not in text and len(text)<=3500
                print(json.dumps({'passed':True,'protocol':init.protocolVersion,'persona':'semiconductor-ai','supplied_file_routing':True,'raw_text_returned':False}))

if __name__=='__main__':asyncio.run(main())
