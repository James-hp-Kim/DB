"""Measure reference retrieval text, not actual billing or model reasoning tokens."""
import json
import os
import sys
import tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump
try:
    import tiktoken
    ENCODER=tiktoken.get_encoding('o200k_base')
except ImportError:
    ENCODER=None

def size(text):
    return {'characters':len(text),'reference_tokens':len(ENCODER.encode(text)) if ENCODER else None}

def main():
    with tempfile.TemporaryDirectory(prefix='backend-payload-') as temporary:
        os.environ['EXPERT_CONTEXT_DIR']=temporary
        choice=kb.available('백엔드',limit=1)
        context=choice['personas'][0]['context']
        cases=[]
        for query,rid in [('DB 연결 풀 고갈','pool-exhaustion'),('느린 쿼리 인덱스','slow-query'),
                          ('p95 동일 조건 비교','latency-comparison'),('7/320 시간초과 재현','lab-limit')]:
            lookup=kb.lookup(query,context=context,limit=2,max_chars=1800)
            rid='backend:'+rid
            assert rid in [r['id'] for r in lookup['matches']]
            read=kb.read([rid],context=context,sections=['conditions','procedure','limits'],max_chars=3000)
            assert all(r['next_offset'] is None for r in read['items'])
            source=kb.sources([read['items'][0]['sources'][0]],context=context,max_chars=2000)
            pieces=[dump(choice),dump(lookup),dump(read),dump(source)]
            cases.append({'query':query,'selected_id':rid,'catalog':size(pieces[0]),'lookup':size(pieces[1]),
                          'read':size(pieces[2]),'source':size(pieces[3]),'first_lookup_total':size('\n'.join(pieces)),
                          'context_reuse_total':size('\n'.join(pieces[1:]))})
        full='\n'.join(p.read_text(encoding='utf-8') for pack in ['backend','common'] for p in sorted((SKILL/f'packs/{pack}/cards').glob('*.md')))
        entry=(SKILL/'SKILL.md').read_text(encoding='utf-8')
        result={'date':'2026-10-30','tokenizer':'o200k_base' if ENCODER else None,
          'scope':'Reference serialized response text. Fixed selected ids/sections. Includes source metadata and first persona search. Excludes user files, prompt, reasoning, answer, protocol/tool schemas; not actual billing savings.',
          'entry_skill_separate':size(entry),'full_backend_common_cards_comparison':size(full),'cases':cases}
        print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
