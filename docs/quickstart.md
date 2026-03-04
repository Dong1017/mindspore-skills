# Quickstart

## Goal

Run one public example and verify the output contract in a few commands.

## 1) Run the example

From repo root:

```bash
bash examples/cpu/plugin_add/run.sh
```

Expected:
- a new folder at `examples/cpu/plugin_add/runs/<run_id>/out/`
- `report.json`, `report.md`, `logs/`, `artifacts/`, `meta/`

## 2) Run contract tests

```bash
python -m pytest -q tests/contract
```

## 3) Run skill-specific tests

```bash
python -m pytest -q skills/cpu-plugin-builder/tests skills/npu-builder/tests skills/mindspore-aclnn-operator-devflow/tests
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
- ensure command is executed from repository root
- check `examples/cpu/plugin_add/run.sh` has execute permission or call with `bash ...`
