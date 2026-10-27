# Current: motion skill overhaul

Updated 2026-10-27.

## Goal

Make `make-editorial-explainer` a stronger Hermes-first skill for source-grounded Vietnamese editorial videos, while keeping a portable core for other agent hosts and preserving Muse/Gemini as capability-gated media providers.

## Done

- Read every tracked Markdown file in `1motion/` plus the helper scripts, JSON schema/templates, HyperFrames kit, and Singapore pilot manifest.
- Confirmed the repository is already at `main`; unrelated `BACKLOG.md`, `HERMES.md`, and `work/` changes remain untouched.
- Added the HyperFrames kit contract and beauty bar in `make-editorial-explainer/references/hf-kit.md`.
- Tightened the skill workflow, README, runtime guidance, and changelog for capability-gated media and playback-based review.
- Fixed motion-event slot validation and added runtime disk/OS diagnostics with regression tests.

## In progress

- Regenerate the package manifest, run helper/schema tests, inspect the pilot render, then commit and push only this session's scoped files.

## Verification limits

- The existing Singapore pilot uses reference-video claims marked pending and is not a publishable final.
- Live Muse/Gemini web media capability remains unverified from this checkout.
