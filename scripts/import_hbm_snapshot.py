"""Explicit HBM research migration into the shared hub; no network or private full text."""
import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
from knowledge import validate_records

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def migrate(snapshot):
    raw=Path(snapshot).read_bytes(); data=json.loads(raw.decode('utf-8-sig'))
    source_path=SKILL/'knowledge/sources.json'; source_before=source_path.read_bytes()
    sources=json.loads(source_before); by_url={s['url'].rstrip('/'):sid for sid,s in sources.items()}
    aliases={}; records=[]; mapping={}; acq={a['id']:a for a in data['acquisitions']}
    for s in data['sources']:
        sid=by_url.get(s['url'].rstrip('/'),'hbm-'+s['id'].lower())
        aliases[s['id']]=sid
        if sid not in sources:
            a=acq.get(s['id'],{})
            sources[sid]={'title':s['title'],'url':s['url'],'kind':s['access'],'checked':s['checked'],
                'limits':s['scope'],'published':s['date'],'legacy_id':s['id'],
                'acquisition':a.get('status','기록 없음'),'review_scope':a.get('review','기존 수집 기록 범위'),
                'bundled_fulltext':False,'migrated':'2026-10-30'}
            if a.get('sha256'):sources[sid]['acquired_file_sha256']=a['sha256']
            by_url[s['url'].rstrip('/')]=sid
        mapping['source:'+s['id']]=sid
    design='hbm-collection-design'
    sources[design]={'title':'HBM 수집·구조화·적용 범위 기록','url':'docs/HBM_DATA.md','kind':'package-design',
        'checked':'2026-10-30','limits':'실험·입력·검토 양식은 설계 제안. 사내 승인·실험 완료 자료 아님.',
        'snapshot_sha256':hashlib.sha256(raw).hexdigest()}
    families=[('MR-MUF','muf','언더필','underfill','TC-NCF','본딩'),('thermal','온도','발열','열','열저항'),
      ('warpage','휨','워페이지'),('hybrid','하이브리드','하이브리드본딩'),('TSV','실리콘관통전극'),
      ('sensor','센서','throttle','스로틀'),('reliability','신뢰성','수명'),('14°C','14도'),
      ('Celsius','섭씨','셀시우스'),('무실패','무고장','0실패'),('JESD','JEDEC','제덱','제이이덱')]
    def add(rid,title,summary,sections,sids,legacy=(),tags=(),evidence='source-linked-summary',track='both'):
        sidlist=list(dict.fromkeys(aliases.get(s,s) for s in sids))
        taglist=list(dict.fromkeys([rid,*legacy,*tags]))
        hay=(title+' '+summary+' '+' '.join(sections.values())).casefold()
        for family in families:
            if any(len(t)>1 and t.casefold() in hay for t in family):
                taglist.extend(t for t in family if t not in taglist)
        for t in re.findall(r'[A-Za-z][A-Za-z0-9-]{2,}',title):
            if t.casefold() not in {'the','and','for','with','from','study','based','using'} and t not in taglist:taglist.append(t)
        record={'id':'hbm:'+rid,'title':title[:180],'summary':summary[:500],'track':track,
            'tags':taglist[:30],'source_ids':sidlist,'evidence_level':evidence,
            'reviewed':data['as_of'],'implementation':'reference-only; no production signoff or physics solver',
            'sections':sections,'legacy_ids':list(legacy)}
        records.append(record)
        for key in legacy:mapping[key]=record['id']
        return record
    def ids(text):return [s.strip() for s in text.split(',') if s.strip()]
    paper_claims=data['claims'][:21]
    for p,c in zip(data['papers'],paper_claims):
        assert p['id'] in ids(c['source_ids'])
        add('paper-'+p['id'].lower(),p['title'],c['statement']+' / '+p['access'],
            {'conditions':p['method']+'\n'+c['statement'],
             'interpretation':p['result']+'\n원문 위치: '+c['locator'],
             'limits':p['limits'], 'verification':p['action'],
             'detail':f"{p['authors']} · {p['year']} · {p['venue']}\nDOI: {p.get('doi','미확인')}\n확보 수준: {p['access']}\n기존 주장 {c['id']}: {c['verdict']}"},
             ids(c['source_ids']),['paper:'+p['id'],'claim:'+c['id']],tags=[p['id'],c['id']],evidence=c['verdict'])
    for i,row in enumerate(data['standards'],28):
        rid,area,title,content,limits,needed,refs=row; c=data['claims'][i-1]
        add('standard-'+rid.lower(),title,content+' / '+limits,
            {'conditions':needed,'procedure':content,'limits':limits,'verification':'승인된 적용 revision·시험조건·판정권자와 대조. 공개 요약을 합격값으로 대입하지 않음.'},
            ids(refs),['standard:'+rid,'claim:'+c['id']],tags=[rid,area])
    for i,row in enumerate(data['tools'],44):
        rid,stage,title,use,io,limits,refs=row; c=data['claims'][i-1]
        add('tool-'+rid.lower(),title,stage+' — '+use,
            {'conditions':io,'procedure':use,'limits':limits+'\nSK hynix 내부 채택·버전·라이선스를 확인한 자료가 아님.',
             'verification':'도구 지원 기능·입력자료·모델·버전 및 실제 프로젝트 승인 흐름을 확인.'},
            ids(refs),['tool:'+rid,'claim:'+c['id']],tags=[rid,stage])
    for i,row in enumerate(data['experiments'],76):
        rid,priority,title,hypothesis,design_text,responses,acceptance,refs=row;c=data['claims'][i-1]
        add('experiment-'+rid.lower(),title,'제안: '+hypothesis,
            {'conditions':design_text,'procedure':hypothesis,'interpretation':responses,'verification':acceptance,
             'limits':'미수행 실험 제안. 개선량·합격값은 미확정이며 사전 baseline과 불확실성을 확인해야 함. 우선순위: '+priority},
             ids(refs),['experiment:'+rid,'claim:'+c['id']],tags=[rid],evidence='proposal-not-executed',track='deep')
    covered={f'claim:F{i:03}' for i in list(range(1,22))+list(range(28,56))+list(range(76,84))}
    # Common survival/acceleration definitions already live in the quality pack.
    for key in ('F060','F061','F062'):
        mapping['claim:'+key]='quality:reliability';covered.add('claim:'+key)
    for c in data['claims']:
        if 'claim:'+c['id'] in covered:continue
        add('claim-'+c['id'].lower(),c['statement'],c['statement'],
            {'conditions':c['locator'],'interpretation':c['statement'],'limits':c['limits'],'verification':c['action']},
            ids(c['source_ids']),['claim:'+c['id']],tags=[c['id'],c['area']],evidence=c['verdict'])
    groups=defaultdict(list)
    for i,row in enumerate(data['data_fields'],1):groups[row[0]].append((i,row))
    for n,(category,items) in enumerate(groups.items(),1):
        lines=[f"DF{i:02} {r[1]} | 단위: {r[2]} | 정의: {r[3]} | 확보: {r[4]} | 이유: {r[5]}" for i,r in items]
        add(f'input-{n:02}',f'HBM 입력자료 — {category}',f'{category} 자료 {len(items)}개 필드. 단위·정의·계측/설계 출처를 함께 받는다.',
            {'conditions':'입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.',
             'procedure':'\n'.join(lines),'limits':'수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.'},
            [design],['field:DF%02d'%i for i,_ in items],tags=[category,'입력자료','데이터',*[r[1][:100] for _,r in items]],evidence='input-template')
    groups=defaultdict(list)
    for r in data['checks']:groups[r[1]].append(r)
    for n,(category,items) in enumerate(groups.items(),1):
        add(f'check-{n:02}',f'HBM 검토 — {category}',f'{category} 검토 {len(items)}개 항목; 초기 상태는 모두 미확인.',
            {'conditions':'제품 범위·승인 규격과 책임자를 먼저 확인.',
             'verification':'\n'.join(f'{r[0]} {r[2]} | 필요 증거: {r[3]} | 상태: {r[4]}' for r in items),
             'limits':'실제 시험 완료/합격 판정이 아니며 사용자 증거 없이는 상태를 바꾸지 않음.'},
            [design],['check:'+r[0] for r in items],tags=[category,'체크','검토'],evidence='unchecked-checklist')
    correction_refs={'R01':['P06'],'R02':['A40'],'R03':['A08'],'R04':['H20','H24'],
      'R05':[],'R06':['P11','A32'],'R07':['A10','A11','A12','A13','A14','A31','A37'],
      'R08':['N02','N03'],'R09':['P01','P02'],'R10':['A22'],'R11':['A24','P11','H22'],'R12':['A11','A41'],'R13':['T09']}
    for row in data['corrections']:
        rid,subject,issue,correction,basis,state=row
        add('correction-'+rid.lower(),subject,correction,
            {'conditions':'기존 해석 주의: '+issue,'interpretation':correction,'verification':basis,
             'limits':f'정정 기록 상태: {state}. 새 독립 실험을 수행했다는 뜻이 아님.'},
            correction_refs[rid] or [design],['correction:'+rid],tags=[rid,'정정'])
    # Make every original source discoverable, without duplicating paper/full-text bodies.
    used={s for r in records for s in r['source_ids']}
    for s in data['sources']:
        if aliases[s['id']] in used:continue
        summary = ('출처 탐색 후보 — '+s['title']+' / '+s['access']) if ('미확보' in s['access'] or '접근 제한' in s['access']) else s['scope']
        add('reference-'+s['id'].lower(),s['title'],summary,
            {'conditions':s['access'],'detail':s['scope'],
             'limits':'출처 탐색용 항목. 원 수집일 이후 재접속·최신 개정 및 모든 본문 주장의 검증은 수행하지 않음.'},
            [s['id']],tags=[s['id'],'문헌목록'],evidence='source-navigation')
    validate_records('hbm',records,sources)
    expected=90+21+85+12+16+8+30+24+13
    assert len(mapping)==expected,(len(mapping),expected)
    all_existing={json.loads(l)['id'] for f in (SKILL/'packs').glob('*/records.jsonl') for l in f.read_text(encoding='utf-8-sig').splitlines() if l.strip()}
    available=all_existing|{r['id'] for r in records}|set(sources)
    assert all(v in available for v in mapping.values())
    if source_path.read_bytes()!=source_before:raise RuntimeError('Shared sources changed during migration; rerun to merge the latest version.')
    write_json(source_path,sources)
    destination=SKILL/'packs/hbm/records.jsonl';destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in records),encoding='utf-8')
    catalog_path=SKILL/'personas/catalog.json';profiles=json.loads(catalog_path.read_text(encoding='utf-8'))
    profiles['hbm-expert']={'label':'HBM 패키징·열·신뢰성 전문가',
      'role':'HBM 패키징·열·신뢰성 관점으로 제품·적층·전력맵·냉각 경계·계측 불확도를 확인한다. 측정·시뮬레이션·회사 발표·제안을 구분하고 평균 ΔT/최대 Tj/열저항 및 오류 사건/불량 칩 분모를 혼용하지 않는다. 필요한 근거와 절만 읽어 가설·확인법·한계를 제시하며 내부 승인값을 만들지 않는다.',
      'keywords':['HBM','HBM 전문가','HBM 패키징','MR-MUF','TC-NCF','언더필','적층','thermal','열저항','warpage','휨','하이브리드 본딩','TSV','열 신뢰성'],
      'default_packs':['hbm'],'allowed_packs':['hbm','common','quality']}
    write_json(catalog_path,profiles)
    report={'migration_date':'2026-10-30','evidence_as_of':data['as_of'],'snapshot_sha256':hashlib.sha256(raw).hexdigest(),
       'source_collection_stats':data['stats'],'legacy_records_mapped':len(mapping),'hbm_records':len(records),
       'shared_generic_records':['quality:reliability'],'source_id_map':aliases,'legacy_to_hub':mapping,
       'notes':['21 paper claims merged into paper records; 16 standard/12 tool/8 experiment claims merged with their records.',
                '30 fields and 24 checks grouped by domain; all original IDs preserved in mapping.',
                'Censoring/Weibull/Arrhenius definitions reuse quality:reliability; explicitly select quality when needed.',
                'No private full text, internal company data or automatic network fetch. Migration is not new source verification.']}
    write_json(BASE/'docs/HBM_IMPORT_PROVENANCE.json',report)
    print(json.dumps({'hbm_records':len(records),'mapped':len(mapping),'sources_total_at_import':len(sources)},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('snapshot',type=Path)
    migrate(parser.parse_args().snapshot)
