# Test report — v1.0.0

## Executed in packaging sandbox, NOT the user's Muse VM
- 8 Python unittest cases: PASS. Includes synthetic audio measurement, synthetic
  video assembly + full decode, stale voice/hash rejection, short clip rejection,
  duplicate/unknown IDs, motion targets, traversal/symlink escape checks,
  final gates/missing assets and init overwrite refusal.
- Example passes stdlib checker for all keywords used by bundled schema.
  Negative case missing narration is rejected. This is NOT full Draft 2020-12
  metaschema validation; jsonschema is not installed, and no package was installed.
- Frontmatter parsed; skill name valid; explicit supporting references exist.
- All Python files compile. Doctor ran without installation or network.
- Assembly integration uses tiny synthetic colour video + tone. It is NOT a
  visual-quality demo, listening test or production benchmark.

## Not executed / not claimed
- Hermes skill discovery on the user's install.
- VieNeu inference (target model/interpreter unavailable here).
- Gemini/9router/Muse media integration or quota verification.
- HyperFrames install/render, finished scene components, full video production.
- Listening/motion review on a real pilot or VM resource benchmark.

## Acceptance still required
Install on Hermes; run discovery; approve story and pilot; verify sources/rights;
implement scene compositions with the installed renderer; watch motion and
listen to voice before calling it production-ready.

Deliverable = workflow skill + helper toolkit, not a self-contained one-command
video application. Review scripts before execution on production.
