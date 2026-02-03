# Overview & Architecture

## Framework Summary

| Aspect | HF Diffusers | MindOne Diffusers |
|--------|--------------|-------------------|
| Base Framework | PyTorch | MindSpore |
| Backend | CUDA | Ascend + GPU |
| Module Base | `torch.nn.Module` | `mindspore.nn.Cell` |
| Forward Method | `forward()` | `construct()` |
| Tensor Type | `torch.Tensor` | `ms.Tensor` |

## Directory Structure

### HF Diffusers
```
src/diffusers/
├── models/      # UNet, VAE, Transformers, ControlNets
├── pipelines/    # 100+ pipeline implementations
├── schedulers/   # Noise schedulers
├── loaders/      # Model loading utilities
├── hooks/        # Hook system
└── utils/        # Utility functions
```

### MindOne Diffusers (changes highlighted)
```
mindone/diffusers/
├── models/      # Same + Flux2, Bria, Kandinsky5, QwenImage
├── pipelines/    # Similar + Flux2, Bria, QwenImage variants
├── schedulers/   # Flax removed
├── loaders/      # Nearly identical
├── hooks/        # + context_parallel.py (NEW)
├── guiders/      # Nearly identical
└── utils/        # + mindspore_utils.py (NEW)
```

## Removed in MindOne

- Flax support files (removed)
- ONNX pipelines (not ported)
- `torch_utils.py` → replaced by `mindspore_utils.py`

## Added in MindOne

| Component | Purpose |
|-----------|---------|
| `hooks/context_parallel.py` | Distributed training for large sequences |
| `utils/mindspore_utils.py` | MindSpore-specific utilities |
| New models | Flux2, Bria, Kandinsky5, QwenImage families |

## Import Differences

```python
# HF Diffusers
import torch
import torch.nn as nn

# MindOne Diffusers
import mindspore as ms
from mindspore import nn, mint  # mint for torch-compatible APIs
```

## Repository Locations

Set `AGENT4HF_ROOT` environment variable (see [env.md](env.md)):
- **HF Diffusers source**: `$AGENT4HF_ROOT/diffusers/src/diffusers`
- **MindOne Diffusers source**: `$AGENT4HF_ROOT/mindone/mindone/diffusers`

## Links

- [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) - Official support status
- [02-api-mapping.md](02-api-mapping.md) - Complete API reference