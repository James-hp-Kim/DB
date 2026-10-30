"""Rebuild DBs and GitHub-readable cards from canonical inputs."""
import json
import os
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
from knowledge import build_store


def main():
    result=build_store(SKILL)
    sources=json.loads((SKILL/'knowledge/sources.json').read_text(encoding='utf-8'))
    index='# 지식 색인\n\n원본 정본에서 생성한 전체 분야의 지식 색인입니다. 페르소나와 독립적으로 저장하며 출처를 공유합니다.\n\n| ID | 제목 | 트랙 | 실행 지원 |\n|---|---|---|---|\n'
    for p in sorted((SKILL/'packs').glob('*/records.jsonl')):
        for line in p.read_text(encoding='utf-8').splitlines():
            r=json.loads(line)
            path=p.parent/'cards'/(r['id'].split(':')[1]+'.md')
            path.parent.mkdir(exist_ok=True)
            body=f"# {r['title']}\n\nID: `{r['id']}` | {r['track']} | {r['implementation']}\n\n{r['summary']}\n"
            for name,text in r['sections'].items(): body+=f'\n## {name}\n\n{text}\n'
            body+='\n## 출처\n\n'
            for sid in r['source_ids']:
                s=sources[sid]; url=s['url']
                if '://' not in url: url=Path(os.path.relpath(BASE/url,path.parent)).as_posix()
                body+=f"- [{s['title']}]({url}) · {s['kind']} · 확인 {s['checked']}\n"
            path.write_text(body,encoding='utf-8')
            index+=f"| `{r['id']}` | [{r['title']}]({path.relative_to(BASE).as_posix()}) | {r['track']} | {r['implementation']} |\n"
    (BASE/'KNOWLEDGE_INDEX.md').write_text(index,encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__': main()
