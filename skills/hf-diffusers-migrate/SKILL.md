---
name: hf-diffusers-migrate
description: Migrate Hugging Face diffusers models to mindone.diffusers. Uses auto_convert.py for automated conversion.
---

# HF Diffusers Migration

Migrate Hugging Face diffusers models (PyTorch) to mindone.diffusers (MindSpore) using automated code conversion.

## When to Use

- Porting Stable Diffusion, SDXL, SD3, Flux, ControlNet, or other diffusion models
- Converting diffusers pipelines to MindSpore framework
- Migrating attention operations for Ascend NPU/GPU backends

## Supported Models

Check [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) for current status (240+ pipelines):
- Base: SD 1.x, SD 2.x, SDXL, SD3, Flux, Flux2
- Video: AnimateDiff, SVD, CogVideoX, Mochi
- Conditioning: ControlNet, LoRA, IP-Adapter, T2I-Adapter
- Text-to-Image: PixArt, Sana, Lumina, AuraFlow

## Workflow

```
1. Analyze HF source → 2. Run auto_convert.py → 3. Manual fixes → 4. Validate
```

## Step 1: Analyze HF Source

Before running conversion, identify dependencies and files to migrate.

**Check support status:**
1. [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) - is model already supported?
2. Note HF diffusers version - API compatibility may vary

**List mindone utility dependencies required:**
```
mindone.diffusers.models.layers_compat
  - scaled_dot_product_attention
  - conv_transpose2d
  - interpolate

mindone.diffusers.utils
  - randn_tensor  (from diffusers.utils.torch_utils)

mindone.diffusers.schedulers.scheduling_utils

mindone.diffusers.utils.outputs
  - TextEncoderOutput
  - BaseModelOutput
```

**Check if HF utilities need migration:**
- `diffusers.utils.torch_utils.randn_tensor` → `mindone.diffusers.utils.mindspore_utils.randn_tensor`
- `diffusers.utils.import_utils` imports
- Pillow `PIL_INTERPOLATION` constants

**List HF files to migrate (by category):**
- Models: `models/unet_2d_condition.py`, `models/vae.py`, `models/transformer_2d.py`
- Pipelines: `pipelines/stable_diffusion/*.py`, `pipelines/flux/*.py`
- Schedulers: `schedulers/*.py`
- Configs: `configs/*.json`, `configuration_*.py`
- Tests: `tests/models/*.py`, `tests/pipelines/*.py`

## Step 2: Run auto_convert.py (Automated Conversion)

**USE THIS FIRST** - The `auto_convert.py` tool handles most conversions automatically.

```bash
# Convert folder
python auto_convert.py --src_root /path/to/hf/diffusers --dst_root /path/to/mindone/diffusers

# Convert single file in place
python auto_convert.py --src_file /path/to/file.py --inplace
```

### Auto-converted by the tool:
| Category | Examples |
|----------|----------|
| Imports | `torch` → `mindspore.mint`, `torch.nn` → `mindspore.nn` |
| Classes | `nn.Module` → `nn.Cell`, `forward()` → `construct()` |
| Tensor operations | 200+ functions (`torch.cat` → `mint.cat`, etc.) |
| Diffusers imports | `diffusers.utils.randn_tensor` → `mindone.diffusers.utils.mindspore_utils.randn_tensor` |
| Cleanup | XLA code blocks, `.to("cuda")` calls |

### What needs manual fixes (logged by converter):
- Unmapped interfaces listed in output
- Conditional device checks: `if torch.cuda.is_available()`
- Dynamic module loading with `importlib`
- Custom attention → use `layers_compat.scaled_dot_product_attention()`
- Parameter keyword differences: `dim=` → `axis=`

## Step 3: Fix Unmapped Interfaces

Review the converter output log and fix reported issues manually.

**Common manual fixes:**
```python
# Tensor method
tensor.numpy() → tensor.asnumpy()

# Device context (set once, not per tensor)
ms.set_context(device_target="Ascend")  # or "GPU"
```

## Step 4: Validate

```python
import numpy as np

# Compare outputs between HF and MindOne
hf_np = hf_output.numpy() if hasattr(hf_output, 'numpy') else hf_output
ms_np = ms_output.asnumpy()
assert np.allclose(hf_np, ms_np, rtol=1e-3, atol=1e-3)
```

## Key API Mappings

| PyTorch | MindSpore |
|---------|-----------|
| `import torch` | `import mindspore as ms` |
| `torch.nn.Module` | `ms.nn.Cell` |
| `forward()` | `construct()` |
| `torch.cat()` | `ms.mint.cat()` |
| `torch.nn.functional.scaled_dot_product_attention` | `mindone.diffusers.models.layers_compat.scaled_dot_product_attention` |

## Reference Documents

| File | Purpose |
|------|---------|
| [01-overview.md](references/01-overview.md) | Framework & architecture overview |
| [02-api-mapping.md](references/02-api-mapping.md) | API mappings |
| [03-migration-guide.md](references/03-migration-guide.md) | Migration workflow |
| [04-support-status.md](references/04-support-status.md) | Support status & priorities |
| [env.md](references/env.md) | Environment setup |
| [guardrails.md](references/guardrails.md) | Migration guidelines |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `torch not defined` | `auto_convert.py` should handle - check unmapped log |
| Shape mismatch | Check `dim` vs `axis` parameter names |
| Accuracy loss | Verify attention mask handling (boolean mask inversion) |

## References

- [mindone.diffusers docs](https://github.com/mindspore-lab/mindone/tree/master/mindone/diffusers)
- [HF diffusers docs](https://huggingface.co/docs/diffusers)
- [layers_compat.py](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/models/layers_compat.py)