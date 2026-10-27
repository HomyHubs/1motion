# HyperFrames Kit Contract

The bundled `templates/hf-kit/` files are a small composition kit, not a renderer and not a media generator. Use them when HyperFrames is available and the project needs a layered editorial scene with stable typography, map geometry, flows, or evidence cards.

## What the kit owns

- Layout tokens for 720×1280 vertical editorial video: safe margins, type scale, dark evidence palette, paper cards, lime/gold/alert semantics, and restrained motion.
- Three scene primitives: `stack` for titles/cards, `map` for routes/places/camera moves, and `flow` for nodes, labeled edges, and tokens.
- A paused GSAP timeline that can seek to any timestamp. The scene must remain deterministic: no timers, random values, network requests, or wall-clock reads.
- Readable text and data as DOM/SVG layers, separate from generated imagery and footage.

## What the kit does not own

- It does not create keyframes, footage, maps, charts, captions, voice, music, or evidence.
- It does not prove a provider can generate media. Record the actual Muse/Gemini capability in `capabilities.json` before requesting an asset.
- It does not replace human review of motion playback, source accuracy, legal status, pronunciation, or rights.

## Scene input contract

The `window.FILM` object should include `composition`, `theme`, `total`, and ordered `beats`. Each beat carries absolute `start`/`end` seconds, a `cues` map, a `visual` object, and `caps`. Cues are absolute timeline seconds, so a visual event should use the narration timing measured from the real WAV rather than a fixed words-per-minute estimate.

`visual.kind` is one of `stack`, `map`, or `flow`.

- `stack`: `stack` items such as `head`, `big`, `label`, `chip`, `card`, `grid`, `split`, and `space`.
- `map`: a `px` object with `top`, `height`, `land`, `routes`, `places`, `labels`, and optional camera keyframes. Route points are explicit `[x, y, rotation, relative_duration]` values.
- `flow`: `nodes`, `edges`, optional `badges`, `swaps`, and a `stack`. Edge `kind` must express the meaning of the relation, such as `cash`, `goods`, `ownership`, `obligation`, or `information`; do not use a decorative arrow where the direction would change the claim.

Every visual should declare its focal order in the project storyboard. Keep source-card screenshots, numbers, chart geometry, map labels, and captions out of generated images so they remain sharp and correctable.

## Production path

1. Run the runtime doctor and record HyperFrames, ffmpeg, Node, CPU, and shared-path status.
2. Obtain or generate the style anchor and media assets through a verified provider route. If Muse/Gemini requires a human web step, create `asset_requests.md` and mark the asset `waiting`; do not replace it with a low-quality placeholder.
3. Build one 15–30 second pilot using at least two scene primitives and real measured voice. Keep the same palette, type system, object IDs, and asset treatment across beats.
4. Preview the first, middle, last frame and every transition. Check that the motion explains the narration, text stays inside safe areas, and evidence/data layers are not warped.
5. Render locally and inspect decoded video, duration, fps, audio, and loudness. Only then assemble the full film.

## Beauty bar

A beautiful result is not a pile of effects. It has one focal point per beat, a clear hierarchy, one meaningful motion event per idea, generous holds for reading, and consistent image treatment. Reject a scene when it is only a poster with a zoom, when a generated image contains text that should be typeset, when a map or chart is approximate, or when the animation changes a relationship without a narrated reason.

## Review record

Store the composition source, provider/capability record, prompt or asset request, render manifest, and review evidence beside the project. Mark visual playback as `not_checked` until a sequence of frames or actual playback has been inspected; a still frame is not motion evidence.
