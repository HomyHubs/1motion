#!/usr/bin/env python3
"""Run with the already verified VieNeu interpreter. No fallback, no install.
Fails on existing outputs: manually archive stale files, or select --only ID.
Offline env guards HF; not a general network sandbox. Cache must be ready.
"""
import argparse
import os
from pathlib import Path
import sys
import tempfile
from project_tools import load, require, inside

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('project');p.add_argument('--voice',default=os.getenv('VIENEU_VOICE','Mai Anh'))
    p.add_argument('--only',nargs='+',help='Beat IDs to synthesize; default all')
    p.add_argument('--cache-confirmed',action='store_true',help='Operator verified complete offline model cache')
    a=p.parse_args()
    if not a.cache_confirmed: p.error('Verify offline cache first, then pass --cache-confirmed')
    root=Path(a.project).expanduser().resolve();doc=load(root);require(doc,root)
    if doc['approvals']['story']!='approved': p.error('Story approval is required before synthesis')
    allids={b['id'] for b in doc['beats']}
    if a.only and not set(a.only)<=allids: p.error('Unknown beat ID')
    selected=[b for b in doc['beats'] if not a.only or b['id'] in a.only]
    for b in selected:
        out=inside(root,b['audio_path'])
        if out.exists(): p.error('Refuse existing WAV: '+str(out))
        if out.suffix.lower()!='.wav': p.error('audio_path must end in .wav')
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    from vieneu import Vieneu
    tts=Vieneu()
    for b in selected:
        out=inside(root,b['audio_path']);out.parent.mkdir(parents=True,exist_ok=True)
        audio=tts.infer(b['narration'],voice=a.voice)
        with tempfile.TemporaryDirectory(prefix='voice-',dir=out.parent) as td:
            tmp=Path(td)/'voice.wav';tts.save(audio,str(tmp))
            if not tmp.is_file() or tmp.stat().st_size<=44: raise ValueError('Missing/empty audio: '+b['id'])
            os.link(tmp,out)
        print('Created',b['id'],out)
    print('Run project_tools.py measure next; listen/review pronunciation separately.')
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as e:
        print('VieNeu batch failed; NO FALLBACK: '+str(e),file=sys.stderr);raise SystemExit(1)
