---
description: Adapt a paper feature or released reference implementation into an existing model codebase and route into algorithm-agent
---

# Feature

Use this as the top-level feature-entry command for adding an algorithm change
into an existing model codebase.

Load the `algorithm-agent` skill and follow its workflow for:

- feature analysis
- integration planning
- patch build
- readiness handoff and report

Use `/feature` when the user is asking:

- add a paper trick
- port a released algorithm feature
- adapt a reference implementation
- add MHC or another model feature into an existing codebase

If the user actually needs model migration rather than feature adaptation,
redirect to `model-agent` or `/migrate`.
