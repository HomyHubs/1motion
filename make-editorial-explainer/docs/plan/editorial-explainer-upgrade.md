# Editorial explainer upgrade plan

## Goal
Make the Hermes/Muse editorial explainer skill deterministic, resumable, source-safe, and capable of producing a polished vertical pilot without silently substituting weak media.

## Ordered work

- [x] P0. Add `scripts/build_film.py` to turn project beats into a seekable HyperFrames `index.html`, and verify the pilot scene ids.
- [x] P0. Re-run the helper suite and record the real count and symlink skip reason in `TEST_REPORT.md`.
- [x] P0. Move the legacy root `SKILL-hermes.md` into `archive/` with a deprecation note, preserving the file rather than deleting it.
- [x] P0. Update the parent CI matrix to Ubuntu 24.04 and Windows, with ffmpeg-aware testing.
- [x] P1. Add phrase cues, word-timestamp cue generation, cue-in-beat validation, and caption guidance.
- [x] P1. Add two-pass loudness normalization and measured ebur128 fields, with `not_checked` until a real output is measured.
- [x] P1. Add scene input hashing and changed-scene resume manifests.
- [x] P1. Keep the ten scene types explicit, documented, and schema-backed; mark unimplemented renderer-specific layouts as planned.
- [x] P1. Add provider capability schema/example and rights validation.
- [x] P1. Add `asset_requests.md` validation and block final rendering while requested assets remain unresolved.
- [x] P2. Add strict JSON Schema validation, Windows CI coverage, and backlog cleanup while preserving the four human-review items.

## Verification

- `python scripts/test_tools.py -v`
- `python scripts/check_schema.py examples/pilot.project.json`
- `python scripts/build_film.py examples/pilot.project.json --out <temporary output>`
- `python scripts/project_tools.py check examples/pilot.project.json`
- CI workflow syntax and matrix reviewed locally; a live run link is only reportable after GitHub execution.

## Explicit limits

- No push, external workflow dispatch, Muse web login, paid provider call, or human playback/listening approval is performed by the local-first run.
- `SKILL-hermes.md` is archived, not deleted.
- Other-session untracked files remain untouched.
