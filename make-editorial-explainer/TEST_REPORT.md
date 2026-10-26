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

## Re-run on Windows (py -3 3.13.15, ffmpeg/ffprobe on PATH)
- `py -3 scripts/test_tools.py`: 12 tests, 11 PASS, 1 SKIP. The skip is `test_symlink_escape`: creating a symlink needs a privilege this account lacks (WinError 1314). The `..` escape is still tested; the symlink escape is tested only where symlinks can be created.
- The original "8 PASS" assumed Linux, ffmpeg and symlink rights. Without ffmpeg, two tests skip.
- Changed tests: `test_init_is_blank` (new: init gives empty sources/claims/assets/beats and `check` rejects it until a title and a beat exist); `test_doctor_honors_env_overrides` (new: VIENEU_PYTHON, VIENEU_VOICE, HYPERFRAMES_CMD reach the doctor report); `test_voice_requires_vieneu_interpreter` (new: `voice` refuses a missing interpreter); `test_path_traversal` split in two; fixtures copy `examples/pilot.project.json` explicitly because `init` now copies `templates/project.template.json`.
- `doctor` resolves VieNeu from `$VIENEU_PYTHON`, else `~/.venvs/vieneu/Scripts/python.exe` (Windows) or `bin/python` (POSIX); the `tts-vi.sh` wrapper probe is gone; `tools.python` reports `sys.executable`; the chromium probes are gone (`hyperframes doctor` owns the browser check); `init` stores no doctor snapshot, doctor runs live at each gate. `py -3 scripts/project_tools.py doctor` on this box now reports `vieneu_python_exists: true`.
- `project_tools.py voice <project> --cache-confirmed [--only ...]` runs `tts_batch.py` with the doctor-resolved VieNeu interpreter. Dispatch checked on this box against a nonexistent project: `tts_batch.py` ran under the VieNeu venv and failed on the missing project.json. This suite runs no synthesis; the VieNeu smoke test belongs to the machine setup, not to these unit tests.
- `assemble()` writes the ffmpeg concat list as UTF-8. The assemble test runs with an ASCII temp path, so a non-ASCII path is unverified.
- SKILL.md is 1.1.0: `<py>` placeholder, `project_tools.py voice` for synthesis, reference-video line in Bước 1. No Hermes load proof yet (see below).
- `check_schema.py` reads UTF-8 explicitly and reports an unsupported schema type instead of raising KeyError.

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
