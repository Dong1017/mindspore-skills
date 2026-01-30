# Guardrails and expectations

## Guardrails
- Avoid custom compatibility wrappers unless required.
- Use diff-based insertion when updating auto maps.
- Keep changes minimal and aligned with existing MindOne patterns.
- Prefer direct API translation over abstraction layers.

## Response expectations
- List reference files consulted (HF diffusers source, mindone.diffusers).
- Summarize edits and note any risks or TODOs.
- Suggest next tests when appropriate (inference validation, weight conversion).
