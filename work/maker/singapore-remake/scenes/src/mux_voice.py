"""Mux measured per-beat voice WAVs onto the rendered silent film. Usage: mux_voice.py <silent.mp4> <out.mp4>"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
src, out = Path(sys.argv[1]), Path(sys.argv[2])
doc = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))
cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(src)]
parts = []
for n, b in enumerate(doc['beats']):
    cmd += ['-i', str(ROOT / b['audio_path'])]
    delay = int(round(b['start_s'] * 1000))
    parts.append(f'[{n + 1}:a]aresample=48000,adelay={delay}|{delay}[a{n}]')
mix = ''.join(f'[a{n}]' for n in range(len(doc['beats'])))
fc = ';'.join(parts) + f';{mix}amix=inputs={len(doc["beats"])}:normalize=0:dropout_transition=0,volume=1.6[aout]'
cmd += ['-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(out)]
subprocess.run(cmd, check=True)
print('wrote', out)
