# Environment Notes

## Workspace Setup

Set the workspace root environment variable to locate or clone repositories:

```bash
# Windows CMD
set AGENT4HF_ROOT=D:\agent4hf_workspace

# Windows PowerShell
$env:AGENT4HF_ROOT="D:\agent4hf_workspace"

# Git Bash / WSL
export AGENT4HF_ROOT="/d/agent4hf_workspace"
```

**For persistence**, add to your shell profile:
- Git Bash: `~/.bashrc`
- WSL: `~/.bashrc`
- Windows PowerShell: Add to `$PROFILE`

**Repository locations**:
- mindone: `$AGENT4HF_ROOT/mindone`
- diffusers: `$AGENT4HF_ROOT/diffusers`

If `AGENT4HF_ROOT` is not set, operations default to the current directory.

## Repository Setup

### MindONE diffusers

```bash
# Clone if not exists
[ -d "$AGENT4HF_ROOT/mindone" ] || git clone https://github.com/mindspore-lab/mindone "$AGENT4HF_ROOT/mindone"

# Install from source (recommended for development)
cd "$AGENT4HF_ROOT/mindone"
pip install -e ".[diffusers]"

# Optional: dev dependencies
pip install -e ".[dev]"      # All dev tools
pip install -e ".[lint,tests]"  # Linting and testing only
```

### HF diffusers

```bash
# Clone if not exists
[ -d "$AGENT4HF_ROOT/diffusers" ] || git clone https://github.com/huggingface/diffusers "$AGENT4HF_ROOT/diffusers"

cd "$AGENT4HF_ROOT/diffusers"
pip install -e .

# Or install from PyPI for reference-only
pip install diffusers
```

## Testing

**mindone/**:
```bash
cd "$AGENT4HF_ROOT/mindone"
pytest tests/diffusers_tests -v
pytest tests/diffusers_tests/pipelines -v
```

**diffusers/**:
```bash
cd "$AGENT4HF_ROOT/diffusers"
make test  # Run full test suite
```

## Environment Quick Reference

```bash
# Set workspace
export AGENT4HF_ROOT="/d/agent4hf_workspace"

# Setup repos
cd "$AGENT4HF_ROOT"
git clone https://github.com/mindspore-lab/mindone
git clone https://github.com/huggingface/diffusers

# Install mindone with diffusers
cd mindone && pip install -e ".[diffusers]"

# Install diffusers
cd ../diffusers && pip install -e .
```