---
description: Diagnose accuracy regressions, numerical drift, wrong-result issues, and cross-platform mismatch after successful execution
---

# Accuracy Agent

Direct specialist entry for accuracy problems after the workload already runs
successfully.

For most users, prefer:

- `/diagnose <problem>` to auto-route into `accuracy-agent` in diagnose mode
- `/fix <problem>` to auto-route into `accuracy-agent` in fix mode

Use `/accuracy-agent` only when you already know the problem is an accuracy
case and want to force the specialist directly.

Load the `accuracy-agent` skill and follow its workflow in either:

- `diagnose` mode for evidence, root cause, and report only
- `fix` mode for diagnose, fix proposal, confirmation, apply, and verify

## Typical Inputs

- symptom description and comparison context
- baseline metrics, outputs, or logs if available
- current metrics, outputs, or logs if available
- earlier readiness snapshot if available
