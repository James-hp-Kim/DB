"""Fixed HBM reference payload benchmark; not model billing or accuracy evaluation."""
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import tiktoken

BASE = Path(__file__).resolve().parents[1]
SKILL = BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump


def main():
    encoder = tiktoken.get_encoding('o200k_base')
    count = lambda text: {'characters':len(text),'reference_tokens':len(encoder.encode(text))}
    skill = (SKILL/'SKILL.md').read_text(encoding='utf-8')
    hbm_reference = (SKILL/'references/hbm.md').read_text(encoding='utf-8')
    entry = skill+'\n'+hbm_reference
    cards = '\n'.join(p.read_text(encoding='utf-8') for p in sorted((SKILL/'packs/hbm/cards').glob('*.md')))
    baseline = count(entry+'\n'+cards)
    cases = []
    with tempfile.TemporaryDirectory(prefix='hbm-benchmark-') as tmp, patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':tmp}):
        choices = kb.available('hbm-expert',limit=1)
        context = choices['personas'][0]['context']
        for query,rid in [('14도','hbm:correction-r09'),('warpage','hbm:paper-a23'),('Celsius','hbm:tool-d05'),('무고장','hbm:claim-f073')]:
            lookup = kb.lookup(query,context=context,limit=2,max_chars=2000)
            sections = ['conditions','procedure' if query=='Celsius' else 'interpretation','limits']
            page = kb.read([rid],context=context,sections=sections,max_chars=3000)
            assert all(x['next_offset'] is None for x in page['items']), 'Incomplete conditions/limits invalidate comparison'
            # All cited source IDs, one per call to avoid silently omitted metadata.
            refs = list(dict.fromkeys(sid for item in page['items'] for sid in item['sources']))
            sources = [kb.sources([sid],context=context,max_chars=3000) for sid in refs]
            assert all(not s['omitted_ids'] for s in sources)
            payload = '\n'.join(dump(x) for x in [choices,lookup,page,*sources])
            scoped = count(entry+'\n'+payload)
            cases.append({'query':query,'selected_id':rid,'expected_in_top2':rid in [x['id'] for x in lookup['matches']],
                'lookup':count(dump(lookup)),'selected_sections':count(dump(page)),
                'all_cited_sources':count('\n'.join(dump(x) for x in sources)),
                'entry_plus_scoped':scoped,'reference_token_reduction_vs_all_cards_percent':round(100*(1-scoped['reference_tokens']/baseline['reference_tokens']),2)})
    print(json.dumps({'date':'2026-10-30','tokenizer':'o200k_base','entry':count(entry),
        'baseline_entry_plus_all_149_hbm_cards':baseline,'cases':cases,
        'limits':'Four fixed queries with preselected relevant IDs; includes full current entry skill + HBM guidance, persona result, lookup, complete selected conditions/result/limits and all cited source metadata. Excludes user inputs, tool definitions/protocol, hidden reasoning, final answer and conversation history. This measures retrieval payload against loading all HBM cards, not billed tokens, general recall, model expertise or accuracy.'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
