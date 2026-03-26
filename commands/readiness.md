---
description: Analyze a local training workspace, validate readiness before training, and route into readiness-agent
---

# Readiness

Use this as the top-level readiness entrypoint before training starts.

Load the `readiness-agent` skill and follow its workflow for:

- workspace analysis
- compatibility validation
- snapshot build
- report build

Use `/readiness` when the user is asking:

- can this repo train
- check my environment before training
- validate my workspace
- run a preflight
- verify config, model, dataset, checkpoint, and environment compatibility

If the workload already runs and the user is reporting a crash, wrong result,
or performance issue, do not stay here. Redirect to:

- `/diagnose`
- `/fix`
