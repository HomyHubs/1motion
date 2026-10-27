# Changelog

All notable changes to the `make-editorial-explainer` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Reproducible Singapore pilot artifacts with measured VieNeu audio, HyperFrames render, geometry input, and explicit human-review limits.
- HyperFrames kit contract covering scene data, capability-gated media inputs, deterministic timelines, and a concrete beauty bar for editorial explainer pilots.

### Changed
- **`make-editorial-explainer`**: sharpened Muse/Gemini media gating, asset handoff requirements, focal-point discipline, playback-based motion review, and runtime diagnostics; bumped the skill to `1.2.0` while keeping project schema `1.0`.

## [1.1.0] - 2026-10-27

### Added
- **Windows & Hermes native compatibility**:
  - Auto-detection for Python virtual environments (`Scripts\python.exe` on Windows vs `bin/python` on POSIX).
  - Subcommand `<py> project_tools.py voice <project>` running VieNeu TTS directly via Python import, removing Linux shell/wrapper dependency (`tts-vi.sh`).
  - Flag `--pilot` for `check` and `assemble` subcommands, allowing review builds without tripping production assertion gates.
  - Template `templates/project.template.json` for clean project initialization without inherited pilot demo data.
  - Configuration example `examples/runtime.env.example` documenting runtime environment variables (`VIENEU_PYTHON`, `VIENEU_VOICE`, `HYPERFRAMES_CMD`).
  - `.gitattributes` pinning LF line endings (`eol=lf`) across `make-editorial-explainer/**` to prevent hash drift in `MANIFEST.sha256` under `core.autocrlf`.
  - Guidelines in `references/story-and-evidence.md` and `SKILL.md` Bước 1 for transcribing and attributing reference video inputs.

### Changed
- **`SKILL.md`**: Bumped skill version to `1.1.0`. Standardized invocation commands using cross-platform `<py>` variable (`py -3` on Windows, `python3` on POSIX).
- **`scripts/project_tools.py`**:
  - `doctor()` now reports dynamic OS and hardware capabilities (`os`, `cpu_count`, `disk_free_gb`, resolved `vieneu_python`, `hyperframes_cmd`), removing hardcoded Linux `/tmp` and static wrapper checks.
  - `assemble()` now forces UTF-8 encoding when generating `concat.txt` for ffmpeg.
  - `init()` copies `project.template.json` instead of `examples/pilot.project.json`.
- **`scripts/check_schema.py`**:
  - Enforced `encoding='utf-8'` on all file reads (fixes H1).
  - Added graceful error handling for unsupported schema types instead of unhandled `KeyError` (fixes H5).
- **`scripts/test_tools.py`**:
  - Guarded symlink traversal test with `try/except OSError` to skip cleanly on Windows without elevated privileges (fixes H3).
  - Added test coverage for `voice` subcommand dispatch and template copying.
- **`README.md` & `references/runtime-hermes.md`**:
  - Separated skill semantic version (`1.1.0`) from project schema version (`1.0`) (fixes H6).
  - Documented Hermes external directory symlink/path integration (`external_dirs`) and first-run online model download requirements.

### Fixed
- UTF-8 decoding crashes on Windows systems running cp1252 code pages.
- `assemble` non-ASCII path failures in ffmpeg concat demuxer.
- Unhandled schema validation crashes on union/null types.
