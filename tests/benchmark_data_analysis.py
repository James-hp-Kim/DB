"""Reference-token payload comparison; does not measure actual Codex billing."""
import json,os,sys,tempfile
from pathlib import Path
import tiktoken
BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump
from profile_data import profile
encoder=tiktoken.get_encoding('o200k_base')
def size(text):return {'characters':len(text),'reference_tokens':len(encoder.encode(text))}
with tempfile.TemporaryDirectory() as temp:
    os.environ['EXPERT_CONTEXT_DIR']=temp
    choice=kb.available('빅데이터',limit=1)
    ctx=choice['personas'][0]['context']
    entry=(SKILL/'SKILL.md').read_text(encoding='utf-8')
    all_cards='\n'.join(p.read_text(encoding='utf-8') for p in sorted((SKILL/'packs').glob('*/cards/*.md')) if p.parents[1].name in ('common','analytics','sales','quality'))
    data=profile(SKILL/'examples/synthetic-monthly.csv',columns=['unique_id','ds','y'],date_column='ds',task='forecast')
    cases=[]
    for query,pack,rid in [('백테스트','sales','sales:backtest'),('WAPE 분모','sales','sales:metrics'),('Optuna pruning','analytics','analytics:hpo'),('대용량 메모리 스트리밍','analytics','analytics:large-data')]:
        found=kb.lookup(query,context=ctx,packs=[pack],max_chars=2500)
        detail=kb.read([rid],context=ctx,packs=[pack],max_chars=3000)
        assert all(x.get('next_offset') is None for x in detail['items'])
        source_ids=list(dict.fromkeys(sid for item in detail['items'] for sid in item['sources']))
        sources=kb.sources(source_ids,context=ctx,packs=[pack])
        assert not sources.get('omitted_ids')
        assert rid in [r['id'] for r in found['matches']]
        retrieval='\n'.join(dump(x) for x in [choice,found,detail,sources])
        cases.append({'query':query,'expected_in_top3':rid in [r['id'] for r in found['matches']],
                      'retrieval_with_sources':size(retrieval),
                      'entry_profile_retrieval':size(entry+'\n'+dump(data)+'\n'+retrieval)})
    result={'date':'2026-10-30','tokenizer':'o200k_base','scope':'Text payload reference only. Includes skill, one persona search, synthetic CSV profile, lookup, selected conditions/procedure/limits and source metadata. Excludes prompts, tool schemas/protocol, reasoning, model replies and other conversation history. Baseline loads all cards in data-analyst allowed packs (common,analytics,sales,quality); not a measured bill or optimal retrieval guarantee.',
            'entry_profile_all_cards':size(entry+'\n'+dump(data)+'\n'+all_cards),'cases':cases}
    print(json.dumps(result,ensure_ascii=False,indent=2))
