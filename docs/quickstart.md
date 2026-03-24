# Quickstart

## Goal

Verify the repository contract and the new top-level skill manifests in a few commands.

## 1) Run contract tests

```bash
python -m pytest -q tests/contract
```

## 2) Run top-level skill tests

```bash
python -m pytest -q \
  skills/readiness-agent/tests \
  skills/failure-agent/tests \
  skills/accuracy-agent/tests \
  skills/performance-agent/tests \
  skills/operator-agent/tests \
  skills/model-agent/tests
```

## Common Issues

1. `pytest` missing:
```bash
python -m pip install pytest
```

2. `jsonschema` / `pyyaml` missing:
```bash
python -m pip install jsonschema pyyaml
```

3. No output generated:
- ensure commands are executed from repository root
- run `python tools/check_consistency.py` to catch registration drift
