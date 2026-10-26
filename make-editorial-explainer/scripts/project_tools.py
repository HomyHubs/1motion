#!/usr/bin/env python3
"""Local helpers, stdlib only. No network, installers, eval or shell=True.
check is intentionally a subset of the bundled JSON Schema, not evidence review.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'map_route','data_compare','source_card','stat_callout','cashflow',
         'transaction_flow','obligation_timeline','document_desk','asset_grid','footage_overlay'}

def run(args):
    return subprocess.run([str(a) for a in args], check=True, capture_output=True, text=True)

def save(path, data):
    path = Path(path)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, encoding='utf-8', delete=False) as f:
        tmp = Path(f.name)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp, path)

def inside(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('Asset paths must be nonempty project-relative strings')
    p = (Path(root) / relative).resolve()
    if not p.is_relative_to(Path(root).resolve()):
        raise ValueError('Path escapes project: ' + relative)
    return p

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def textsha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def probe(path):
    info = json.loads(run(['ffprobe','-v','error','-show_entries',
                          'format=duration:stream=codec_type,width,height,r_frame_rate',
                          '-of','json',path]).stdout)
    duration = float(info['format']['duration'])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Invalid duration: ' + str(path))
    return duration, info

def load(root):
    return json.loads((Path(root) / 'project.json').read_text(encoding='utf-8'))

def validate(doc, root, assets=False, final=False):
    errors = []
    if not isinstance(doc, dict):
        return ['Project must be an object']
    for key in ['version','title','mode','format','approvals','sources','claims','assets','beats']:
        if key not in doc:
            errors.append('Missing ' + key)
    if errors:
        return errors
    if doc['version'] != '1.0': errors.append('Unsupported version')
    if not isinstance(doc['title'],str) or not doc['title'].strip(): errors.append('Empty title')
    if doc['mode'] not in ['script_only','pilot','full']: errors.append('Invalid mode')
    fmt = doc['format']
    if not isinstance(fmt,dict):
        errors.append('format must be an object'); fmt = {}
    for k in ['width','height','fps']:
        if type(fmt.get(k)) is not int or fmt[k] <= 0: errors.append('Invalid format.' + k)
    for k in ['width','height']:
        if type(fmt.get(k)) is int and fmt[k] % 2: errors.append(k + ' must be even for yuv420p')
    if not isinstance(doc['approvals'],dict):
        errors.append('approvals must be object'); approvals={}
    else: approvals=doc['approvals']
    for k in ['story','pilot']:
        if approvals.get(k) not in ['pending','approved','rejected']: errors.append('Invalid approval ' + k)
        if final and approvals.get(k) != 'approved': errors.append('Approval pending/rejected: ' + k)
    sets = {}
    for key in ['sources','claims','assets','beats']:
        rows = doc[key]
        if not isinstance(rows,list):
            errors.append(key + ' must be array'); sets[key]={}; continue
        ids={}
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id']:
                errors.append('Invalid item/id in ' + key); continue
            if row['id'] in ids: errors.append('Duplicate id in ' + key + ': ' + row['id'])
            ids[row['id']]=row
        sets[key]=ids
    if not sets.get('beats'): errors.append('At least one beat required')
    for source in sets.get('sources',{}).values():
        if not source.get('title'): errors.append('Source missing title: '+source['id'])
        if source.get('path'):
            try: inside(root,source['path'])
            except ValueError as e: errors.append(str(e))
    for c in sets.get('claims',{}).values():
        if c.get('type') not in ['fact','attributed','allegation','analysis','forecast']: errors.append('Invalid claim type: '+c['id'])
        if c.get('status') not in ['verified','pending','illustrative']: errors.append('Invalid claim status: '+c['id'])
        refs=c.get('source_ids')
        if not isinstance(refs,list): errors.append('Missing source_ids: '+c['id']); refs=[]
        for ref in refs:
            if ref not in sets['sources']: errors.append('Unknown source: '+str(ref))
        if c.get('status')=='verified' and not refs: errors.append('Verified claim has no source: '+c['id'])
    for a in sets.get('assets',{}).values():
        try:
            p=inside(root,a.get('path'))
            if assets and not p.is_file(): errors.append('Missing asset: '+a['id'])
        except ValueError as e: errors.append(str(e))
        if a.get('status') not in ['ready','waiting','placeholder']: errors.append('Invalid asset status: '+a['id'])
        if final and (a.get('status')!='ready' or not a.get('rights_note','').strip()): errors.append('Asset not cleared: '+a['id'])
    for b in sets.get('beats',{}).values():
        bid=b['id']
        if not re.fullmatch(r'[A-Za-z0-9_-]+',bid): errors.append('Unsafe beat id: '+bid)
        for key in ['narration','purpose']:
            if not isinstance(b.get(key),str) or not b[key].strip(): errors.append('Missing '+key+': '+bid)
        if b.get('scene_type') not in TYPES: errors.append('Invalid scene type: '+bid)
        tail=b.get('tail_s')
        if type(tail) not in [int,float] or not math.isfinite(tail) or tail<0: errors.append('Invalid tail: '+bid)
        for key,pool in [('claim_ids','claims'),('asset_ids','assets')]:
            refs=b.get(key)
            if not isinstance(refs,list): errors.append('Missing '+key+': '+bid); continue
            for ref in refs:
                if ref not in sets[pool]: errors.append('Unknown '+pool+' ref: '+str(ref))
                elif final and pool=='claims' and sets[pool][ref].get('status')=='pending': errors.append('Unverified used claim: '+ref)
        layerids=set()
        if not isinstance(b.get('layers'),list): errors.append('Missing layers: '+bid)
        else:
            for layer in b['layers']:
                if not isinstance(layer,dict) or not layer.get('id') or not layer.get('role'): errors.append('Invalid layer: '+bid)
                else:
                    if layer['id'] in layerids: errors.append('Duplicate layer: '+bid)
                    layerids.add(layer['id'])
        if not isinstance(b.get('events'),list): errors.append('Missing events: '+bid)
        else:
            for e in b['events']:
                if not isinstance(e,dict) or any(not e.get(k) for k in ['target','trigger_phrase','action','meaning']): errors.append('Invalid motion event: '+bid); continue
                if e['target'] not in layerids: errors.append('Unknown event target: '+bid)
                if e['trigger_phrase'] not in b.get('narration',''): errors.append('Trigger not in narration: '+bid)
                if 'time_s' in e and (type(e['time_s']) not in [int,float] or not math.isfinite(e['time_s']) or e['time_s']<0): errors.append('Invalid event time: '+bid)
                elif 'time_s' in e and 'slot_duration_s' in b and e['time_s']>=b['slot_duration_s']: errors.append('Event outside slot: '+bid)
        for key in ['audio_path','clip_path']:
            try:
                p=inside(root,b.get(key))
                if final and not p.is_file(): errors.append('Missing '+key+': '+bid)
            except ValueError as e: errors.append(str(e))
    return errors

def require(doc,root,**kwargs):
    errors=validate(doc,root,**kwargs)
    if errors: raise ValueError('\n'.join(errors))

def measure(root):
    root=Path(root);doc=load(root); require(doc,root)
    start=0.0
    for b in doc['beats']:
        p=inside(root,b['audio_path']);dur,_=probe(p)
        if b.get('narration_sha256') and b['narration_sha256'] != textsha(b['narration']) and b.get('audio_sha256') == sha(p):
            raise ValueError('Narration changed but WAV unchanged; regenerate voice first: '+b['id'])
        b.update(audio_duration_s=round(dur,6),slot_duration_s=round(dur+b['tail_s'],6),
                 start_s=round(start,6),audio_sha256=sha(p),narration_sha256=textsha(b['narration']))
        start+=b['slot_duration_s']
    doc['total_duration_s']=round(start,6)
    save(root/'project.json',doc)
    return doc

def assemble(root):
    root=Path(root).resolve();doc=load(root);require(doc,root,assets=True,final=True)
    fmt=doc['format'];fps=fmt['fps'];outdir=root/'final';outdir.mkdir(exist_ok=True)
    output=outdir/'film.mp4'
    if output.exists(): raise ValueError('Refuse overwrite final/film.mp4; archive it explicitly first')
    inputs=[]
    for b in doc['beats']:
        wav=inside(root,b['audio_path']);clip=inside(root,b['clip_path'])
        if b.get('narration_sha256')!=textsha(b['narration']) or b.get('audio_sha256')!=sha(wav):
            raise ValueError('Stale/missing voice hashes; regenerate if narration changed, then measure: '+b['id'])
        dur,_=probe(wav); cd,info=probe(clip)
        if not any(s.get('codec_type')=='video' for s in info['streams']): raise ValueError('No video stream: '+str(clip))
        slot=dur+b['tail_s']
        if cd+1/fps+0.005 < slot: raise ValueError('Clip too short for voice+tail: '+b['id'])
        if abs(b.get('slot_duration_s',-1)-slot)>0.005: raise ValueError('Stale timing: '+b['id'])
        inputs.append((b,clip,wav,slot))
    segments=[]
    with tempfile.TemporaryDirectory(prefix='assemble-',dir=outdir) as temp:
        temp=Path(temp)
        for n,(b,clip,wav,slot) in enumerate(inputs):
            seg=temp/f'{n:04d}.mp4'
            filt=(f'[0:v]setpts=PTS-STARTPTS,scale={fmt["width"]}:{fmt["height"]}:'
                  f'force_original_aspect_ratio=decrease,pad={fmt["width"]}:{fmt["height"]}:'
                  f'(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},tpad=stop_mode=clone:stop_duration=0.1[v];'
                  f'[1:a]asetpts=PTS-STARTPTS,aresample=48000,apad,atrim=duration={slot:.6f}[a]')
            run(['ffmpeg','-v','error','-nostdin','-y','-i',clip,'-i',wav,'-filter_complex',filt,
                 '-map','[v]','-map','[a]','-t',f'{slot:.6f}','-c:v','libx264','-preset','veryfast',
                 '-crf','20','-threads','1','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2',seg])
            segments.append(seg)
        listing=temp/'concat.txt'
        listing.write_text(''.join("file '"+str(p).replace("'","'\\''")+"'\n" for p in segments),encoding='utf-8')
        rendered=temp/'joined.mp4'
        run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',listing,'-c','copy','-movflags','+faststart',rendered])
        run(['ffmpeg','-v','error','-nostdin','-i',rendered,'-f','null','-'])
        dur,info=probe(rendered)
        expected=sum(row[3] for row in inputs)
        if abs(dur-expected)>len(inputs)/fps+0.08: raise ValueError('Unexpected mux duration drift')
        # Atomic non-overwrite publish, even if another process raced this helper.
        os.link(rendered,output)
    manifest={'scope':'basic local VO-only assembly; not visual/evidence/listening approval',
              'measured_duration_s':dur,'expected_duration_s':expected,'file':str(output.relative_to(root)),
              'sha256':sha(output),'inputs':[{'id':b['id'],'clip_sha256':sha(c),'audio_sha256':sha(w),'slot_s':d} for b,c,w,d in inputs]}
    save(outdir/'assembly_manifest.json',manifest)
    return manifest

def init(root):
    root=Path(root)
    if root.exists(): raise ValueError('Refuse existing project directory')
    root.mkdir(parents=True)
    for d in ['audio','assets','sources','scenes','captions','final','logs']: (root/d).mkdir()
    shutil.copyfile(ROOT/'templates/project.template.json',root/'project.json')
    save(root/'capabilities.json',{'status':'unverified','providers':[],'shared_filesystem':'unverified'})
    shutil.copyfile(ROOT/'templates/REVIEW.md',root/'REVIEW.md')

def vieneu_python():
    override=os.environ.get('VIENEU_PYTHON')
    if override: return Path(override)
    return Path.home()/'.venvs/vieneu'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')

def voice(root,extra):
    interpreter=vieneu_python()
    if not interpreter.is_file(): raise ValueError('VieNeu interpreter not found: '+str(interpreter)+' (set VIENEU_PYTHON)')
    return subprocess.run([str(interpreter),str(ROOT/'scripts/tts_batch.py'),str(root),*extra]).returncode

def doctor():
    tools={k:shutil.which(k) for k in ['ffmpeg','ffprobe','node']}
    tools['python']=sys.executable
    tools['hyperframes']=os.environ.get('HYPERFRAMES_CMD') or shutil.which('hyperframes')
    vieneu=vieneu_python()
    return {'tools':tools,'python':sys.version.split()[0],'cpu_count':os.cpu_count(),
            'vieneu_python':str(vieneu),'vieneu_python_exists':vieneu.is_file(),
            'vieneu_voice':os.environ.get('VIENEU_VOICE'),
            'notice':'Paths only. No installation, network, model import, media endpoint or benchmark performed.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['doctor','init','check','measure','assemble','voice'])
    parser.add_argument('project',nargs='?');parser.add_argument('--assets',action='store_true');parser.add_argument('--final',action='store_true')
    args,extra=parser.parse_known_args()
    if extra and args.command!='voice': parser.error('unrecognized arguments: '+' '.join(extra))
    if args.command=='doctor': result=doctor()
    else:
        if not args.project: parser.error('project required')
        root=Path(args.project).expanduser().resolve()
        if args.command=='init': init(root);result={'created':str(root)}
        elif args.command=='check':
            errors=validate(load(root),root,args.assets,args.final);print(json.dumps({'ok':not errors,'errors':errors},ensure_ascii=False,indent=2));return int(bool(errors))
        elif args.command=='voice': return voice(root,extra)
        elif args.command=='measure': result={'total_duration_s':measure(root)['total_duration_s']}
        else: result=assemble(root)
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:
        print('ERROR: '+str(e),file=sys.stderr)
        if isinstance(e,subprocess.CalledProcessError): print((e.stderr or '')[-2500:],file=sys.stderr)
        raise SystemExit(1)
