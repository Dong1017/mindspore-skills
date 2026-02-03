# Migration Workflow

**FIRST: Use `auto_convert.py` for automated conversion**

```
HF Diffusers → auto_convert.py → Manual Fixes → Validation
```

## Using auto_convert.py

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
- Unmapped interfaces in output
- Conditional device checks: `if torch.cuda.is_available()`
- Dynamic module loading with `importlib`
- Custom attention → use `layers_compat.scaled_dot_product_attention()`
- Parameter keyword differences: `dim=` → `axis=`

## Post-Conversion Manual Fixes

After running `auto_convert.py`, address:

### Tensor method (may need manual fix if .numpy() still exists)
```python
tensor.numpy() → tensor.asnumpy()
```

### Device context (set once, not per tensor)
```python
ms.set_context(device_target="Ascend")  # or "GPU"
```

### Attention (May need manual attention)
```python
from mindone.diffusers.models.layers_compat import scaled_dot_product_attention
output = scaled_dot_product_attention(q, k, v, attn_mask=mask, backend="flash")
```

## Validation

```python
import numpy as np

# Compare outputs between HF and MindOne
hf_np = hf_output.numpy() if hasattr(hf_output, 'numpy') else hf_output
ms_np = ms_output.asnumpy()
assert np.allclose(hf_np, ms_np, rtol=1e-3, atol=1e-3)
```

## Common Issues

| Issue | Fix |
|-------|-----|
| `torch not defined` | `auto_convert.py` should handle - check unmapped log |
| `.numpy()` error | Change to `.asnumpy()` - may need manual fix |
| Module vs Cell | `auto_convert.py` handles this automatically |

## References

- [02-api-mapping.md](02-api-mapping.md) - Complete API reference
- [04-support-status.md](04-support-status.md) - Current support status matrix