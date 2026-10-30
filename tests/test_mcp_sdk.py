"""Optional official MCP Python SDK interoperability check; no Codex auth required."""
import asyncio
import json
import sys
import os
import tempfile
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    base=Path(__file__).resolve().parents[1]
    script=base/'plugins/expert-hub/skills/expert/scripts/mcp_server.py'
    receipt_dir=tempfile.TemporaryDirectory(prefix='expert-sdk-')
    params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(script)],env={**os.environ,'EXPERT_CONTEXT_DIR':receipt_dir.name})
    async with stdio_client(params) as streams:
        async with ClientSession(*streams) as session:
            initialized=await session.initialize()
            listing=await session.list_tools()
            assert len(listing.tools)==5
            choices=await session.call_tool('expert_catalog',{'query':'품질보증','limit':1})
            context=json.loads(choices.content[0].text)['personas'][0]['context']
            found=await session.call_tool('expert_lookup',{'query':'불량률 분모','context':context})
            assert not found.isError
            hits=json.loads(found.content[0].text)['matches']
            assert 'common:data-contract' in [r['id'] for r in hits]
            page=await session.call_tool('expert_read',{'ids':['quality:weco-rules'],'sections':['procedure'],'context':context})
            assert not page.isError and '연속 8점' in page.content[0].text
            sources=await session.call_tool('expert_source',{'ids':json.loads(page.content[0].text)['items'][0]['sources'],'context':context})
            assert not sources.isError
            chip=await session.call_tool('expert_catalog',{'query':'chip-design-verification','limit':1})
            chip_context=json.loads(chip.content[0].text)['personas'][0]['context']
            routed=await session.call_tool('expert_reference_input',{'file':str(base/'examples/chip-timing-synthetic.rpt'),'context':chip_context})
            assert not routed.isError
            assert 'rtl:c22' in [r['id'] for r in json.loads(routed.content[0].text)['retrieval']['matches']]
            rejected=await session.call_tool('expert_reference_input',{'file':str(base/'examples/chip-timing-synthetic.rpt'),'context':context})
            assert rejected.isError
            print(json.dumps({'passed':True,'protocol':initialized.protocolVersion,'tools':[t.name for t in listing.tools],'chip_file_reference':True,'wrong_persona_rejected':True},ensure_ascii=False))

    receipt_dir.cleanup()

if __name__=='__main__': asyncio.run(main())
