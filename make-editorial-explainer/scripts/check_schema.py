#!/usr/bin/env python3
"""Stdlib checker for keywords used by bundled schema, NOT a full JSON Schema engine.
For third-party schema compliance use a separately approved Draft 2020-12 validator.
"""
import json
from pathlib import Path
import re
import sys

def check(s,v,path='$'):
    errors=[]
    kinds={'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),
           'string':lambda x:isinstance(x,str),'integer':lambda x:type(x)is int,
           'number':lambda x:type(x)in(int,float)}
    if 'type'in s and not kinds[s['type']](v): return [path+': wrong type']
    if 'const'in s and v!=s['const']: errors.append(path+': wrong const')
    if 'enum'in s and v not in s['enum']: errors.append(path+': wrong enum')
    if isinstance(v,dict):
        for key in s.get('required',[]):
            if key not in v: errors.append(path+': missing '+key)
        for key,sub in s.get('properties',{}).items():
            if key in v: errors.extend(check(sub,v[key],path+'.'+key))
    if isinstance(v,list):
        if len(v)<s.get('minItems',0): errors.append(path+': too few items')
        if 'items'in s:
            for i,x in enumerate(v): errors.extend(check(s['items'],x,path+f'[{i}]'))
    if isinstance(v,str):
        if len(v)<s.get('minLength',0): errors.append(path+': too short')
        if 'pattern'in s and not re.search(s['pattern'],v): errors.append(path+': pattern mismatch')
    if type(v)in(int,float):
        if 'minimum'in s and v<s['minimum']: errors.append(path+': below minimum')
        if 'exclusiveMinimum'in s and v<=s['exclusiveMinimum']: errors.append(path+': below exclusive minimum')
    return errors

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    doc=Path(sys.argv[1]) if len(sys.argv)>1 else root/'examples/pilot.project.json'
    errors=check(json.loads((root/'templates/project.schema.json').read_text()),json.loads(doc.read_text()))
    print(json.dumps({'ok':not errors,'scope':'bundled schema keyword subset; not full metaschema validation','errors':errors},ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))
