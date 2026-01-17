# External Integrations

**Analysis Date:** 2026-01-17

## APIs & External Services

**None detected:**
- No external API clients or SDKs found
- No network communication libraries (requests, httpx, etc.)
- Fully offline tool

## Data Storage

**Databases:**
- None
  - No database connections or ORMs
  - No SQLite usage detected

**File Storage:**
- Local filesystem only
  - Input: `.scr` bytecode files (binary format)
  - Output: `.c` source files, `.asm` disassembly, `.json` symbol tables
  - Cache: `.validation-baseline.json` (regression testing baseline)
  - Working directory: Temporary files for compilation validation

**Caching:**
- Custom file-based caching for validation results
  - Implementation: `vcdecomp/validation/cache.py`
  - Cache location: Temporary directory (managed by ValidationCache)
  - Purpose: Avoid recompiling unchanged decompiled sources

## Authentication & Identity

**Auth Provider:**
- Not applicable
  - Desktop CLI/GUI tool with no authentication

## Monitoring & Observability

**Error Tracking:**
- None
  - No external error tracking services (Sentry, Rollbar, etc.)

**Logs:**
- Python logging module (standard library)
  - Location: `vcdecomp/validation/validator.py`, `vcdecomp/validation/compiler_wrapper.py`
  - Output: Console/stderr
  - No centralized logging service integration

## CI/CD & Deployment

**Hosting:**
- Not applicable
  - Desktop application, not hosted

**CI Pipeline:**
- None detected
  - No GitHub Actions, GitLab CI, or other CI configuration files
  - No .github/workflows/ directory

## Environment Configuration

**Required env vars:**
- None
  - All configuration via CLI arguments

**Secrets location:**
- Not applicable
  - No secrets or credentials required

## Webhooks & Callbacks

**Incoming:**
- None
  - No web server or webhook endpoints

**Outgoing:**
- None
  - No webhook calls or external notifications

## External Tools Integration

**Legacy Vietcong Compiler Toolchain:**
- Integration with proprietary Windows executables via subprocess
  - Location: `original-resources/compiler/`
  - Tools:
    - `scmp.exe` - Main compiler orchestrator
    - `spp.exe` - Preprocessor
    - `scc.exe` - C to assembly compiler
    - `sasm.exe` - Assembly to bytecode assembler
  - Wrapper: `vcdecomp/validation/compiler_wrapper.py`
  - Purpose: Recompile decompiled source to validate output correctness
  - Communication: stdin/stdout/stderr via subprocess.run()
  - Timeout: 30 seconds default (`vcdecomp/validation/compiler_wrapper.py:69`)

**Test Framework:**
- pytest
  - Integration: Test discovery and execution
  - Location: `vcdecomp/tests/`
  - No pytest.ini or configuration file detected

---

*Integration audit: 2026-01-17*
