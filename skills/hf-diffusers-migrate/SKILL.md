---
name: hf-diffusers-migrate
description: Migrate Hugging Face diffusers models to mindone.diffusers. Use when porting Stable Diffusion, SDXL, ControlNet, or other diffusion models.
---

# HF Diffusers Migration

Migrate Hugging Face diffusers models to MindOne's diffusers implementation.

## When to Use

- Porting Stable Diffusion models to MindSpore
- Migrating SDXL, ControlNet, LoRA adapters
- Converting diffusers pipelines to mindone
- Adding new diffusion model architectures
- Converting attention operations for MindSpore (Ascend/GPU)

## Target Repository & Versions

**mindone.diffusers**: https://github.com/mindspore-lab/mindone

**Version Compatibility**: Check the official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) for current version compatibility. MindOne tracks HF diffusers releases and provides support for new versions.

**Note**: Version compatibility evolves as mindone tracks new HF diffusers releases. Always check the latest version information in the mindone repository.

### Checking Support Status

See the official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) in the mindone repository for the current support matrix showing:
- Which pipelines are verified with fp32/fp16/bf16 precision
- Inference verification status with official weights
- 240+ diffusion pipelines supported

## Supported Model Types

- **Base Models**: SD 1.x, SD 2.x, SDXL, SD3, Flux, Flux2
- **ControlNet**: Various conditioning models
- **Adapters**: LoRA, IP-Adapter, T2I-Adapter
- **Video**: AnimateDiff, SVD, CogVideoX, Mochi, etc.
- **Text-to-Image**: PixArt, Sana, Lumina, AuraFlow, etc.
- **Inpainting/Outpainting**: Specialized pipelines

## Quick Start

```python
# Basic import mapping example
# HF (PyTorch):
#   import torch
#   from torch.nn import Linear, Conv2d

# MindOne (MindSpore):
import mindspore as ms
from mindspore import nn
from diffusers.models.layers_compat import (
    conv_transpose2d,
    interpolate,
    scaled_dot_product_attention,
    group_norm,
)

# Model classes have similar APIs but use nn.Cell instead of nn.Module
from diffusers import UNet2DConditionModel

model = UNet2DConditionModel.from_pretrained("path/to/mindspore/weights")
```

## Instructions

### Step 1: Analyze Source Model

1. Identify the HF diffusers model architecture
2. Check if similar architecture exists in mindone.diffusers (see official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md))
3. Document API differences between HF and mindone
4. Note the HF diffusers version - API mappings may differ by version

### Step 2: Import Mapping

Replace PyTorch imports with MindSpore equivalents:

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `import torch` | `import mindspore as ms` | Main framework |
| `torch.nn.Module` | `mindspore.nn.Cell` | Base class |
| `forward()` | `construct()` | Method name |
| `torch.Tensor` | `ms.Tensor` | Type annotation |
| `F.scaled_dot_product_attention` | `scaled_dot_product_attention` | From layers_compat |
| `F.conv_transpose2d` | `conv_transpose2d` | From layers_compat |
| `F.interpolate` | `interpolate` | From layers_compat |

### Step 3: Model Migration

1. Replace `nn.Module` with `nn.Cell`
2. Rename `forward()` to `construct()`
3. Use `layers_compat` for version-aware operations
4. Update tensor operations (`dim` → `axis`, `.numpy()` → `.asnumpy()`)

### Step 4: Weight Conversion

1. Download HF model weights
2. Map weight names to MindOne format if needed
3. Convert using conversion utilities or save as safetensors

### Step 5: Validation

1. Run inference with same inputs on both frameworks
2. Compare outputs numerically (target: rtol=1e-3, atol=1e-3)
3. Benchmark performance

## Key Differences from HF Diffusers

1. **Framework**: PyTorch → MindSpore (supports Ascend NPU and GPU)
2. **Module Base**: `nn.Module` → `nn.Cell`
3. **Forward Method**: `forward()` → `construct()`
4. **Attention**: Uses `layers_compat.scaled_dot_product_attention()`
5. **Flax/ONNX removed**: Only MindSpore backend supported
6. **Context Parallel**: Added distributed training support via `hooks/context_parallel.py`
7. **New Models**: Flux2, Bria, Kandinsky5, QwenImage

## Analysis Documentation

See `references/` directory for detailed analysis:

- [00-overview.md](references/00-overview.md) - Executive summary and version compatibility
- [01-architecture-overview.md](references/01-architecture-overview.md) - High-level structure comparison
- [02-api-mapping.md](references/02-api-mapping.md) - Detailed PyTorch to MindSpore API mappings
- [03-folder-structure.md](references/03-folder-structure.md) - Folder-by-folder comparison
- [04-model-architecture.md](references/04-model-architecture.md) - Specific model implementation differences
- [05-mindone-specific.md](references/05-mindone-specific.md) - Components unique to mindone
- [06-pipeline-migration.md](references/06-pipeline-migration.md) - Step-by-step migration workflow

## Examples

### Example 1: Simple Model Conversion

```python
# Before (HF/PyTorch)
import torch.nn as nn

import torch.nn.functional as F

class SimpleBlock(nn.Module):
    def forward(self, x):
        x = F.conv_transpose2d(x, self.weight, stride=2)
        return x

# After (MindOne)
import mindspore as ms
from mindspore import nn
from diffusers.models.layers_compat import conv_transpose2d

class SimpleBlock(nn.Cell):
    def construct(self, x):
        x = conv_transpose2d(x, self.weight, stride=2)
        return x
```

### Example 2: Attention Layer

```python
# Before (HF/PyTorch)
import torch.nn.functional as F

def attention(q, k, v, mask=None):
    return F.scaled_dot_product_attention(q, k, v, attn_mask=mask, is_causal=True)

# After (MindOne)
from diffusers.models.layers_compat import scaled_dot_product_attention

def attention(q, k, v, mask=None):
    return scaled_dot_product_attention(q, k, v, attn_mask=mask, is_causal=True, backend="flash")
```

## Troubleshooting

**Problem**: `AttributeError: module 'torch' has no attribute '...'`
**Solution**: Replace torch operations with MindSpore equivalents (see API mapping)

**Problem**: Shape mismatch after migration
**Solution**: Check `dim` vs `axis` parameter names in reduction operations

**Problem**: Accuracy degradation
**Solution**: Verify attention mask handling - MindSpore uses inverted boolean masks

## References

- [mindone.diffusers documentation](https://github.com/mindspore-lab/mindone/tree/master/mindone/diffusers)
- [HF diffusers documentation](https://huggingface.co/docs/diffusers)
- [layers_compat.py source](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/models/layers_compat.py)