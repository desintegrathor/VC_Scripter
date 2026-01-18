---
phase: 03-ci-cd-pipeline
plan: 01
subsystem: infrastructure
tags: [github-actions, self-hosted-runner, windows-service, ci-cd]

# Dependency graph
requires:
  - phase: 02-test-suite-automation
    provides: "Pytest test suite for automated validation"
provides:
  - "Self-hosted Windows GitHub Actions runner"
  - "Runner service with automatic startup"
  - "Access to SCMP.exe compiler for CI validation"
affects: [03-ci-cd-pipeline-02, 03-ci-cd-pipeline-03, 04-error-analysis-reporting]

# Tech tracking
tech-stack:
  added: [github-actions-runner, windows-service]
  patterns: ["One-time infrastructure setup with checkpoints", "Service installation via PowerShell", "GitHub runner registration"]

key-files:
  created:
    - C:\actions-runner\install-service.ps1
    - C:\actions-runner\.runner
    - C:\actions-runner\config.cmd
  modified: []

key-decisions:
  - "Self-hosted runner required for Windows-only SCMP.exe compiler"
  - "Runner installed as Windows service for persistence and auto-start"
  - "Service installation via PowerShell script with elevated privileges"

patterns-established:
  - "Pattern 1: GitHub runner registration requires web UI token generation (1-hour expiry)"
  - "Pattern 2: Service installation separate from runner configuration"
  - "Pattern 3: Runner verification via GitHub API (gh api repos/.../actions/runners)"

# Metrics
duration: 15min
completed: 2026-01-18
---

# Phase 03 Plan 01: Self-Hosted Runner Setup Summary

**Self-hosted Windows GitHub Actions runner installed and configured as Windows service with access to SCMP.exe compiler**

## Performance

- **Duration:** 15 min
- **Tasks:** 4 (2 auto, 2 checkpoints)
- **Infrastructure created:** GitHub Actions runner service

## Accomplishments
- Downloaded and installed GitHub Actions runner for Windows x64
- Configured runner with repository registration token
- Installed runner as Windows service with automatic startup
- Verified runner online status and compiler accessibility
- Enabled CI/CD pipeline for automated validation

## Task Execution

### Task 1: Download GitHub Actions Runner
- **Status:** ✓ Completed
- **Commit:** a864195 (from previous execution wave)
- **Result:** Runner binaries extracted to C:\actions-runner
- **Files:** config.cmd, run.cmd, bin/RunnerService.exe

### Task 2: Generate GitHub runner registration token (checkpoint:human-action)
- **Status:** ✓ Completed
- **Action:** User generated registration token via GitHub web UI
- **Token validity:** 1 hour (standard GitHub limitation)
- **Resume signal:** User provided token

### Task 3: Configure and Install Runner
- **Status:** ✓ Completed (continuation execution)
- **Actions performed:**
  - Extracted GitHub username from git remote: desintegrathor
  - Ran configuration: `config.cmd --url https://github.com/desintegrathor/VC_Scripter --token [TOKEN] --labels windows,x64 --runasservice --name "VC-Scripter-Windows-Runner"`
  - Installed Windows service via install-service.ps1
  - Started service: `sc.exe start "actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner"`
- **Service status:** Running (Automatic startup)
- **Runner status:** Online and Idle
- **Files created:** C:\actions-runner\.runner (registration metadata)

### Task 4: Verify Runner Online (checkpoint:human-verify)
- **Status:** ✓ Verified
- **Verifications performed:**
  1. GitHub API check: Runner status = "online", busy = false
  2. Service status: Running with StartType = Automatic
  3. Compiler accessibility: SCMP.exe path verified
  4. Runner labels: self-hosted, Windows, X64
- **Result:** Runner ready to accept CI jobs

## Files Created/Modified

### Created:
- `C:\actions-runner\install-service.ps1` - PowerShell script to install and start runner service
  ```powershell
  sc.exe create "actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner" binPath= "C:\actions-runner\bin\RunnerService.exe" start= auto DisplayName= "GitHub Actions Runner (VC-Scripter-Windows-Runner)"
  sc.exe start "actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner"
  ```

- `C:\actions-runner\.runner` - Runner registration metadata
  - agentId: 2
  - agentName: VC-Scripter-Windows-Runner
  - poolName: Default
  - gitHubUrl: https://github.com/desintegrathor/VC_Scripter

- `C:\actions-runner\config.cmd` - Runner configuration script (from runner package)
- `C:\actions-runner\run.cmd` - Runner execution script (from runner package)

### Modified:
None - infrastructure setup only

## Decisions Made

**Self-hosted runner approach:**
- Rationale: SCMP.exe is Windows-only DOS-era executable, cannot run on GitHub-hosted Ubuntu/macOS runners
- Alternative considered: Wine emulation (rejected - unreliable for DOS executables)
- Impact: Requires machine to remain online for CI jobs

**Windows service installation:**
- Rationale: Ensures runner auto-starts on reboot, runs as background service
- Alternative considered: Interactive runner (rejected - requires user login)
- Implementation: PowerShell script with sc.exe for service management

**Runner labels configuration:**
- Rationale: Enables workflow targeting with `runs-on: [self-hosted, windows, x64]`
- Labels: self-hosted, Windows, X64 (default), windows, x64 (custom)
- Impact: Workflows can explicitly target this runner type

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Service installation not completed at checkpoint**
- **Found during:** Continuation from Task 2 checkpoint
- **Issue:** User indicated "done" but service was not actually installed. Runner was registered (C:\actions-runner\.runner exists) but service status query returned no results, GitHub API showed runner "offline"
- **Fix:** Executed install-service.ps1 via PowerShell with elevated privileges to install and start the Windows service
- **Files modified:** None (infrastructure only)
- **Verification:** Service query returned "Running" status, GitHub API returned "online" status
- **Result:** Runner now fully operational and ready for CI jobs

---

**Total deviations:** 1 auto-fixed (1 blocking issue - incomplete service installation)
**Impact on plan:** Required automatic completion of service installation step to unblock plan. This was a critical blocker preventing runner from being operational.

## Service Configuration

**Service name:** `actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner`
**Display name:** GitHub Actions Runner (VC-Scripter-Windows-Runner)
**Executable:** C:\actions-runner\bin\RunnerService.exe
**Start type:** Automatic
**Status:** Running

**Service management commands:**
```powershell
# Check status
Get-Service -Name 'actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner'

# Start service
sc.exe start "actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner"

# Stop service
sc.exe stop "actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner"

# Query service status
sc.exe query "actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner"
```

## Runner Verification

**GitHub API verification:**
```bash
gh api repos/desintegrathor/VC_Scripter/actions/runners
```

**Expected response:**
```json
{
  "total_count": 1,
  "runners": [{
    "id": 2,
    "name": "VC-Scripter-Windows-Runner",
    "os": "Windows",
    "status": "online",
    "busy": false,
    "labels": [
      {"name": "self-hosted", "type": "read-only"},
      {"name": "Windows", "type": "read-only"},
      {"name": "X64", "type": "read-only"}
    ]
  }]
}
```

**Compiler accessibility:**
```powershell
Test-Path C:\Users\flori\source\repos\VC_Scripter\original-resources\compiler\SCMP.exe
# Returns: True
```

## Next Phase Readiness

**Phase 3 Plan 02 (Create CI Workflow) - READY:**
- Self-hosted runner is online and idle
- Runner has "self-hosted", "windows", "x64" labels for workflow targeting
- Runner service account can access repository and SCMP.exe
- Can proceed with .github/workflows/validation.yml creation

**Phase 3 Plan 03 (Test CI Pipeline) - READY:**
- Runner will execute workflow jobs automatically
- Service configured for automatic startup (survives reboots)
- GitHub API integration tested and working

**No blockers for next phases.**

## Maintenance Notes

**Runner persistence:**
- Service configured for automatic startup on system boot
- Machine must remain online to accept CI jobs
- Runner heartbeats to GitHub every 50 seconds

**Security considerations:**
- Runner runs with service account privileges
- Has read/write access to repository checkout (_work directory)
- Can execute arbitrary code from workflow definitions (standard GitHub Actions behavior)

**Runner updates:**
- GitHub Actions runner auto-updates when new versions are released
- Service restart may be required for updates
- Monitor runner version in GitHub settings UI

**Troubleshooting:**
- Check service status: `Get-Service -Name 'actions.runner.desintegrathor-VC_Scripter.VC-Scripter-Windows-Runner'`
- Check runner logs: `C:\actions-runner\_diag\` directory
- Restart service if offline: `sc.exe stop [service-name] && sc.exe start [service-name]`

---
*Phase: 03-ci-cd-pipeline*
*Completed: 2026-01-18*
