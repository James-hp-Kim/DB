"""Persona knowledge and local QA analysis CLI. Base runtime needs only Python."""
import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

from qa_core import VERSION,digest,dump
import knowledge as kb


def parser():
    root=argparse.ArgumentParser(description=__doc__)
    commands=root.add_subparsers(dest='command',required=True)
    cmd=commands.add_parser('reference-input'); cmd.add_argument('file',type=Path)
    cmd.add_argument('--context',required=True); cmd.add_argument('--query')
    cmd.add_argument('--max-chars',type=int,default=3500)
    cmd=commands.add_parser('profile'); cmd.add_argument('file',type=Path)
    cmd.add_argument('--columns',nargs='+'); cmd.add_argument('--date-column')
    cmd.add_argument('--task',choices=['general','forecast','sales','quality'],default='general')
    cmd.add_argument('--max-rows',type=int,default=100000); cmd.add_argument('--max-chars',type=int,default=3500)
    cmd.add_argument('--encoding',default='utf-8-sig')
    cmd=commands.add_parser('catalog'); cmd.add_argument('query')
    cmd.add_argument('--limit',type=int,default=3); cmd.add_argument('--offset',type=int,default=0)
    commands.add_parser('status'); commands.add_parser('build')
    for name in ('lookup','read'):
        cmd=commands.add_parser(name)
        cmd.add_argument('--context',required=True)
        cmd.add_argument('--packs',nargs='+')
        cmd.add_argument('--include-private',action='store_true')
        cmd.add_argument('--max-chars',type=int,default=3500 if name=='lookup' else 6000)
        if name=='lookup':
            cmd.add_argument('query'); cmd.add_argument('--limit',type=int,default=3)
            cmd.add_argument('--track',choices=['quick','deep','both'],default='both')
        else:
            cmd.add_argument('ids',nargs='+'); cmd.add_argument('--sections',nargs='+')
            cmd.add_argument('--offset',type=int,default=0)
    cmd=commands.add_parser('source'); cmd.add_argument('ids',nargs='+')
    cmd.add_argument('--context',required=True); cmd.add_argument('--packs',nargs='+')
    cmd.add_argument('--include-private',action='store_true'); cmd.add_argument('--max-chars',type=int,default=5000)
    cmd=commands.add_parser('ingest-note'); cmd.add_argument('file',type=Path)
    cmd.add_argument('--store',type=Path,required=True); cmd.add_argument('--title',required=True)
    for name in ('scan','monitor','anomalies'):
        cmd=commands.add_parser(name); cmd.add_argument('file',type=Path)
        cmd.add_argument('--out',type=Path,required=True); cmd.add_argument('--encoding',default='utf-8-sig')
        if name=='scan':
            cmd.add_argument('--values',nargs='*',default=[]); cmd.add_argument('--groups',nargs='*',default=[])
            cmd.add_argument('--numerator'); cmd.add_argument('--denominator'); cmd.add_argument('--category')
            cmd.add_argument('--numerator-type',choices=['units','events'],default='units')
        elif name=='monitor':
            cmd.add_argument('--value',required=True); cmd.add_argument('--mean',type=float,required=True)
            cmd.add_argument('--sigma',type=float,required=True); cmd.add_argument('--order')
            cmd.add_argument('--baseline-validated',action='store_true')
            cmd.add_argument('--ewma-lambda',type=float,default=.2); cmd.add_argument('--cusum-k',type=float,default=.5)
            cmd.add_argument('--cusum-h',type=float,default=5.)
        else:
            cmd.add_argument('--values',nargs='+',required=True); cmd.add_argument('--top',type=int,default=10)
    return root


def main(argv=None):
    args=vars(parser().parse_args(argv)); command=args.pop('command')
    try:
        if command=='reference-input':
            from input_reference import reference_input
            result=reference_input(**args)
        elif command=='profile':
            from profile_data import profile
            result=profile(**args)
        elif command=='build': result=kb.build_store(kb.ROOT)
        elif command in ('catalog','status'): result={'catalog':kb.available,'status':kb.status}[command](**args)
        elif command in ('lookup','read','source','ingest-note'):
            result={'lookup':kb.lookup,'read':kb.read,'source':kb.sources,'ingest-note':kb.ingest_note}[command](**args)
        else:
            from analysis import scan,monitor,anomalies,save_result,concise
            source=args.pop('file'); out=args.pop('out')
            options={'command':command,**args}
            fingerprint=hashlib.sha256((digest(source)+dump(options)+VERSION).encode('utf-8')).hexdigest()
            if (out/'result.json').exists():
                existing=json.loads((out/'result.json').read_text(encoding='utf-8'))
                if existing.get('fingerprint')!=fingerprint: raise FileExistsError('Different input/options/version; choose a new --out')
                result=concise({'cached':True,'result':existing,'output':str(out.resolve())})
            else:
                if out.exists(): raise FileExistsError('Output already exists; choose a new --out')
                data={'scan':scan,'monitor':monitor,'anomalies':anomalies}[command](source,**args)
                result=concise(save_result(data,source,options,out))
        print(dump(result)); return 0
    except (ValueError,KeyError,OSError,UnicodeError,OverflowError,sqlite3.Error,csv.Error) as exc:
        sys.stderr.write(dump({'error':type(exc).__name__,'message':str(exc)})+'\n'); return 2


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
