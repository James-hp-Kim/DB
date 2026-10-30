"""Reference-text size comparison; not a billing or answer-quality benchmark."""
import json,os,sys,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
S=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(S/'scripts'))
import knowledge as kb
from qa_core import dump

def main():
    import tiktoken
    enc=tiktoken.get_encoding('o200k_base')
    count=lambda text:len(enc.encode(text))
    entry=(S/'SKILL.md').read_text(encoding='utf-8')+(S/'references/semiconductor-ai.md').read_text(encoding='utf-8')
    scenarios=[('hold slack','chip-rtl','claim-c06'),('barrel','chip-rtl','config-barrel'),
               ('DRAM HBM SRAM SSD','chip-memory','model-levels'),('noise','chip-analog','claim-c34')]
    rows=[]
    with tempfile.TemporaryDirectory() as d:
        os.environ['EXPERT_CONTEXT_DIR']=d
        for query,pack,rid in scenarios:
            catalog=kb.available('semiconductor-ai',limit=1)
            context=catalog['personas'][0]['context']
            found=kb.lookup(query,context=context,packs=[pack],limit=2,max_chars=2400)
            ids=[r['id'] for r in found['matches']]
            expected=pack+':'+rid
            assert expected in ids,(query,ids)
            read=kb.read([expected],context=context,packs=[pack],sections=['conditions','limits'],max_chars=2400)
            source_ids=next(r for r in found['matches'] if r['id']==expected)['sources']
            sources=kb.sources(source_ids[:2],context=context,packs=[pack],max_chars=2500)
            selected=entry+'\n'+ '\n'.join(map(dump,[catalog,found,read,sources]))
            full=entry+'\n'+ '\n'.join(p.read_text(encoding='utf-8') for p in sorted((S/'packs'/pack/'cards').glob('*.md')))
            a,b=count(full),count(selected)
            rows.append({'query':query,'pack':pack,'selected_id':expected,'full_pack_reference_tokens':a,'selected_reference_tokens':b,'reference_reduction_pct':round(100*(1-b/a),2),'selected_response_chars':sum(len(dump(x)) for x in [catalog,found,read,sources])})
    result={'date':'2026-10-30','tokenizer':'tiktoken o200k_base','tiktoken_version':tiktoken.__version__,'scope':'Entry skill + routing guide are included on both sides. Full selected pack Markdown compared with catalog + 2 hits + conditions/limits for 1 id + at most 2 sources. Excludes user/system messages, reasoning, tool schemas, retries and final answers. Not actual Codex billing or accuracy. Four authored fixed queries; no generalization.','rows':rows}
    (BASE/'docs/SEMICONDUCTOR_AI_BENCHMARK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
