import json, sys, time
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
model_name = sys.argv[3] if len(sys.argv) > 3 else 'large-v3-turbo'
t0 = time.time()
model = WhisperModel(model_name, device='cpu', compute_type='int8')
segments, info = model.transcribe(src, language='vi', beam_size=5, vad_filter=True)
rows = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segments]
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'model': model_name, 'language': info.language, 'duration': info.duration, 'elapsed_s': round(time.time() - t0, 1), 'segments': rows}, f, ensure_ascii=False, indent=1)
with open(out.replace('.json', '.txt'), 'w', encoding='utf-8') as f:
    for r in rows:
        f.write(f"[{r['start']:7.2f}-{r['end']:7.2f}] {r['text']}\n")
print('TRANSCRIBE_OK', len(rows), round(time.time() - t0, 1))
