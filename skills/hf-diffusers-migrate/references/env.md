# Environment Notes

## MindOne diffusers setup
```bash
# Install from source (recommended for development)
cd mindone
pip install -e ".[diffusers]"

# Install with optional dependencies
pip install -e ".[dev]"      # All dev tools
pip install -e ".[lint,tests]"  # Linting and testing only
```

## HF diffusers setup
```bash
cd diffusers
pip install -e .

# Or install from PyPI
pip install diffusers
```

## Code quality & formatting
**diffusers/** uses Makefile and ruff:
```bash
# Format code
make style                    # Format all files with ruff
make quality                  # Run all linting checks

# Fix everything
make fixup                    # Run style, quality, and consistency checks
```

**mindone/** uses pyproject.toml configuration:
- Formatting: Black (line length 120)
- Import sorting: isort with MindSpore-specific sections

## Testing

**mindone/**:
```bash
# Run diffusers tests
pytest tests/diffusers_tests -v

# Run specific pipeline test
pytest tests/diffusers_tests/pipelines -v
```
