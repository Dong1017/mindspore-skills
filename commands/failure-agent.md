---
description: Diagnose MindSpore and PTA (torch_npu) training and runtime failures by analyzing evidence, validating likely root causes, and emitting an actionable report
---

# Failure Agent

Direct specialist entry for training and runtime failures across MindSpore and
PTA (PyTorch + torch_npu).

For most users, prefer:

- `/diagnose <problem>` to auto-route into `failure-agent` in diagnose mode
- `/fix <problem>` to auto-route into `failure-agent` in fix mode

Use `/failure-agent` only when you already know the problem is a failure case
and want to force the specialist directly.

Load the `failure-agent` skill and follow its workflow in either:

- `diagnose` mode for evidence, root cause, and report only
- `fix` mode for diagnose, fix proposal, confirmation, apply, and verify

## Typical Inputs

- full traceback or error log
- framework versions and backend/device details
- exact failing command and runtime context
- previous readiness snapshot if available
