"""Reference payload tokens for fixed chip-review scenarios, not model billing."""
import json
import os
import sys
import tempfile
from pathlib import Path

import tiktoken

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump
from mcp_server import TOOLS
from input_reference import reference_input


def main():
    encoder=tiktoken.get_encoding('o200k_base')
    count=lambda value:len(encoder.encode(value))
    skill=(SKILL/'SKILL.md').read_text(encoding='utf-8')
    cards='\n'.join(p.read_text(encoding='utf-8') for p in sorted((SKILL/'packs/rtl/cards').glob('*.md')))
    all_cards_tokens=count(skill+'\n'+cards)
    cases=[]
    with tempfile.TemporaryDirectory(prefix='chip-token-check-') as temp:
        os.environ['EXPERT_CONTEXT_DIR']=temp
        choice=kb.available('chip-design-verification',limit=1)
        context=choice['personas'][0]['context']
        for query,rid in [('비동기 FIFO 포인터','rtl:c09'),('STA WNS TNS setup hold','rtl:c22'),('refresh self-refresh debt','rtl:c13'),('num_bitflips 장치 매핑 분모','rtl:g02')]:
            found=kb.lookup(query,context=context,max_chars=2500)
            detail=kb.read([rid],sections=['conditions','verification' if rid!='rtl:g02' else 'interpretation','limits'],context=context,max_chars=3000)
            source_ids=list(dict.fromkeys(s for r in detail['items'] for s in r['sources']))
            sources=kb.sources(source_ids[:5],context=context,max_chars=3000)
            payload='\n'.join(map(dump,[choice,found,detail,sources]))
            with_entry=count(skill+'\n'+payload)
            cases.append({'query':query,'record':rid,'expected_in_top3':rid in [r['id'] for r in found['matches']],
                'retrieval_reference_tokens':count(payload),'entry_plus_retrieval_reference_tokens':with_entry,
                'reduction_against_entry_and_all_rtl_cards_percent':round(100*(1-with_entry/all_cards_tokens),2),
                'read_continuations':sum(x.get('next_offset') is not None for x in detail['items']),
                'source_omitted_ids':sources.get('omitted_ids',[])})
        file_result=reference_input(BASE/'examples/chip-timing-synthetic.rpt',context=context)
    result={'date':'2026-10-30','tokenizer':'o200k_base','scope':'Fixed test cases; includes one catalog response, lookup, 3 selected sections and selected source metadata per case. Not autonomous task success, exact Codex tokenizer, actual total tokens or billing. Excludes user prompt/files, reasoning, final answer, conversation history and protocol framing. Tool definitions measured separately.',
      'entry_skill_reference_tokens':count(skill),'entry_plus_all_141_rtl_cards_reference_tokens':all_cards_tokens,
      'all_tool_definitions_reference_tokens':count(dump(TOOLS)),
      'input_route_example':{'response_characters':len(dump(file_result)),'reference_tokens':count(dump(file_result)),'raw_file_lines_returned':0},
      'cases':cases}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(x['expected_in_top3'] for x in cases): raise SystemExit(1)


if __name__=='__main__':main()
