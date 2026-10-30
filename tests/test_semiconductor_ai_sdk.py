"""Optional official MCP SDK test; install mcp separately for this maintainer test."""
import asyncio,json,os,sys,tempfile
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
BASE=Path(__file__).resolve().parents[1]

def error(result):
    return getattr(result,'is_error',getattr(result,'isError',None))

async def main():
    with tempfile.TemporaryDirectory(prefix='반도체 MCP ') as d:
        p=Path(d)/'설계 조건.sdc';p.write_text('PRIVATE_TEST\nset_multicycle_path 2 -setup\n',encoding='utf-8')
        params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(BASE/'plugins/expert-hub/skills/expert/scripts/mcp_server.py')],env={**os.environ,'EXPERT_CONTEXT_DIR':str(Path(d)/'contexts')})
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                initialized=await session.initialize()
                listing=await session.list_tools()
                cat=await session.call_tool('expert_catalog',{'query':'semiconductor-ai','limit':1})
                c=json.loads(cat.content[0].text)['personas'][0]['context']
                found=await session.call_tool('expert_lookup',{'query':'hold slack','context':c,'packs':['chip-rtl'],'limit':2,'max_chars':2000})
                assert not error(found)
                assert 'chip-rtl:claim-c06' in [x['id'] for x in json.loads(found.content[0].text)['matches']]
                body=await session.call_tool('expert_read',{'ids':['chip-rtl:claim-c06'],'sections':['conditions','limits'],'context':c,'packs':['chip-rtl'],'max_chars':2400})
                assert not error(body)
                source=await session.call_tool('expert_source',{'ids':['chip-public-experiment'],'context':c,'packs':['chip-rtl']})
                assert not error(source)
                routed=await session.call_tool('expert_reference_input',{'file':str(p),'context':c,'max_chars':2500})
                assert not error(routed),routed
                assert json.loads(routed.content[0].text)['selected_pack']=='chip-rtl'
                assert 'PRIVATE_TEST' not in routed.content[0].text
                denied=await session.call_tool('expert_lookup',{'query':'x','context':c,'packs':['backend']})
                assert error(denied)
                result={'passed':True,'tools':[x.name for x in listing.tools],'persona':'semiconductor-ai','checks':['catalog','lookup','read','source','reference_input','scope rejection'],'protocol':getattr(initialized,'protocol_version',getattr(initialized,'protocolVersion',None))}
                print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':asyncio.run(main())
