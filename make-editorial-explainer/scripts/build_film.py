#!/usr/bin/env python3
"""Build a deterministic HyperFrames HTML composition from a project JSON file."""
import argparse
import html
import json
from pathlib import Path

SCENE_KINDS = {"map_route": "map", "transaction_flow": "flow", "cashflow": "flow"}


def scene_for_beat(beat, start, end):
    kind = SCENE_KINDS.get(beat.get("scene_type"), "stack")
    visual = {"kind": kind, "kicker": beat.get("purpose", "")}
    if kind == "stack":
        visual["stack"] = [{"type": "head", "text": beat.get("narration", ""), "id": beat["id"]}]
    elif kind == "flow":
        visual["nodes"] = [{"id": layer["id"], "x": 360, "y": 420 + i * 190, "text": layer.get("role", layer["id"]), "icon": "box"} for i, layer in enumerate(beat.get("layers", []))]
        visual["edges"] = []
    else:
        visual["px"] = {"top": 150, "height": 520, "land": [], "routes": [], "places": [], "labels": []}
    return {"id": beat["id"], "start": start, "end": end, "cues": {}, "visual": visual, "caps": []}


def build(project_path, out_dir):
    project = json.loads(Path(project_path).resolve().read_text(encoding="utf-8"))
    start = 0.0
    beats = []
    for beat in project.get("beats", []):
        duration = float(beat.get("slot_duration_s") or beat.get("audio_duration_s") or 3.0) + float(beat.get("tail_s", 0))
        beats.append(scene_for_beat(beat, round(start, 6), round(start + duration, 6)))
        start += duration
    film = {"composition": project.get("title", "editorial-explainer"), "theme": "geo", "total": round(start, 6), "beats": beats}
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(film, ensure_ascii=False, separators=(",", ":"))
    scenes = " ".join(f'<meta name="scene-id" content="{html.escape(b["id"])}">' for b in beats)
    document = "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">{scenes}<title>{title}</title><link rel=\"stylesheet\" href=\"kit.css\"></head><body><main id=\"root\"><div id=\"film\"></div></main><script>window.FILM={payload};</script><script src=\"gsap.min.js\"></script><script src=\"kit.js\"></script></body></html>".format(scenes=scenes, title=html.escape(project.get("title", "Editorial explainer")), payload=payload)
    (out_dir / "index.html").write_text(document, encoding="utf-8")
    (out_dir / "film.json").write_text(json.dumps(film, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out_dir / "index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    build(args.project, args.out)
