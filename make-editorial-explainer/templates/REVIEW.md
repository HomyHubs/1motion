# REVIEW
- Project/version/date:
- Gate 1 approval (user/source/time): pending
- Gate 2 approval (user/source/time): pending
- Tools/versions actually used:
- Local/remote/manual stages:
- Costs verified / unknown:

| Check | pass/fail/not_checked | Evidence / limitation |
|---|---|---|
| Sources support claims | not_checked | |
| Legal status / data semantics | not_checked | |
| Map accuracy and attribution | not_checked | |
| Visual keyframes and transitions | not_checked | |
| Motion playback | not_checked | |
| Voice listened / pronunciation | not_checked | |
| Caption sync | not_checked | |
| Audio mix / clipping | not_checked | Two-pass loudnorm target `I=-16:TP=-1:LRA=11`; ebur128 measurement not_checked until run on final output. |
| Full decode / format / duration | not_checked | |
| CPU/RAM benchmark | not_checked | |
| Resume changed-scene test | not_checked | `build/manifest.json` records per-scene input hashes; run the one-scene mutation test before release. |

## Changes required
## Human review still needed
## Reproduce / edited files
