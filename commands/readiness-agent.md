---
description: Analyze a local single-machine training workspace, validate readiness before training, and emit a reusable snapshot and report
---

# Readiness Agent

Direct specialist entry for training workspace readiness before execution.

For most users, prefer:

- `/readiness <workspace or problem>`

Use `/readiness-agent` only when you already know you want to force the
readiness specialist directly.

Load the `readiness-agent` skill and follow its workflow:

1. workspace analysis
2. compatibility validation
3. snapshot build
4. report build

## Typical Inputs

- code folder or working directory
- train config, model, dataset, or checkpoint paths if already known
- framework hints if the user already knows them
