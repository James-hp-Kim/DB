"""Bounded CSV profiling for knowledge routing; never returns raw example rows."""
import csv
import hashlib
import math
from datetime import date
from pathlib import Path
from qa_core import dump


def profile(file, columns=None, date_column=None, task='general', max_rows=100000,
            max_chars=3500, encoding='utf-8-sig'):
    if type(max_rows) is not int or max_rows < 0:
        raise ValueError('max_rows >= 0; 0 explicitly scans all rows')
    if type(max_chars) is not int or not 1500 <= max_chars <= 12000:
        raise ValueError('max_chars: 1500..12000')
    if task not in ('general','forecast','sales','quality'):
        raise ValueError('Invalid task')
    path=Path(file)
    if path.suffix.lower() != '.csv':
        raise ValueError('CSV required; convert other formats locally first')
    before=path.stat()
    with path.open(encoding=encoding,newline='') as stream:
        reader=csv.reader(stream,strict=True)
        headers=next(reader,[])
        if not headers or any(not h.strip() for h in headers) or len(set(headers))!=len(headers):
            raise ValueError('Missing/blank/duplicate column names')
        selected=headers[:12] if columns is None else columns
        if not selected or len(selected)>30 or len(set(selected))!=len(selected) or not set(selected)<=set(headers):
            raise ValueError('Select 1..30 existing unique columns')
        if date_column is not None and date_column not in selected:
            raise ValueError('date_column must be one of the selected columns')
        indices=[headers.index(c) for c in selected]
        stats=[{'name':c,'missing':0,'numeric':0,'nonfinite':0,'zero':0,'negative':0,
                'min':None,'max':None} for c in selected]
        # shortcut: capped distinct digests are lower bounds, not exact cardinalities above 256.
        unique=[set() for _ in selected]; capped=[False]*len(selected)
        dates={'column':date_column,'valid':0,'invalid':0,'min':None,'max':None} if date_column else None
        count=0; truncated=False
        for row in reader:
            if max_rows and count>=max_rows:
                truncated=True; break
            if len(row)!=len(headers):
                raise ValueError(f'Column count mismatch at CSV record {count+2}')
            count+=1
            for i,col in enumerate(indices):
                value=row[col].strip(); stat=stats[i]
                if not value:
                    stat['missing']+=1; continue
                value_hash=hashlib.blake2b(value.encode('utf-8'),digest_size=16).digest()
                if value_hash not in unique[i]:
                    if len(unique[i])<256: unique[i].add(value_hash)
                    else: capped[i]=True
                try:
                    numeric=float(value)
                except ValueError:
                    numeric=None
                if numeric is not None:
                    if math.isfinite(numeric):
                        stat['numeric']+=1; stat['zero']+=numeric==0; stat['negative']+=numeric<0
                        stat['min']=numeric if stat['min'] is None else min(stat['min'],numeric)
                        stat['max']=numeric if stat['max'] is None else max(stat['max'],numeric)
                    else: stat['nonfinite']+=1
                if dates and stat['name']==date_column:
                    try:
                        if len(value)!=10: raise ValueError('Expected YYYY-MM-DD')
                        parsed=date.fromisoformat(value).isoformat()
                        dates['valid']+=1
                        dates['min']=min(dates['min'],parsed) if dates['min'] else parsed
                        dates['max']=max(dates['max'],parsed) if dates['max'] else parsed
                    except ValueError: dates['invalid']+=1
        for i,stat in enumerate(stats):
            stat['distinct_at_least']=len(unique[i])+int(capped[i])
            stat['distinct_capped']=capped[i]
    after=path.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise ValueError('Input changed while profiling; retry a stable snapshot')
    queries=[{'packs':['analytics'],'query':'데이터 프로파일 전처리'}]
    if task in ('forecast','sales'):
        queries.append({'packs':['sales'],'query':'백테스트' if task=='forecast' else '매출 정의 통화'})
    elif task=='quality': queries.append({'packs':['quality'],'query':'SPC 관리도 선택'})
    if before.st_size>100*1024*1024:
        queries.append({'packs':['analytics'],'query':'대용량 메모리 스트리밍'})
    result={'rows_scanned':count,'complete_scan':not truncated,'sampling':'file prefix; not random',
            'file_bytes':before.st_size,'column_count':len(headers),'columns':stats,
            'columns_not_profiled':len(headers)-len(selected),'columns_omitted_from_response':0,
            'dates':dates,'suggested_lookups':queries,
            'note':'Counts describe scanned rows only. Numeric-looking IDs remain strings. Dates require explicit YYYY-MM-DD column. No raw rows/values, duplicate-key check, calendar continuity check or company-data ingestion. Search persona first; pass its context to lookup/read/source.'}
    while len(dump(result))>max_chars and result['columns']:
        result['columns'].pop(); result['columns_omitted_from_response']+=1
    if len(dump(result))>max_chars: raise ValueError('Budget too small; shorten column names or increase max_chars')
    return result
