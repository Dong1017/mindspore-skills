# Pipeline Migration Guide

This document provides a step-by-step workflow for migrating HuggingFace diffusers pipelines to mindone.diffusers.

## Migration Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HF Diffusers (PyTorch)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Analyze Source Model                                 │
│   - Identify pipeline components                              │
│   - Check model architecture                                  │
│   - Review dependencies                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Import Mapping                                        │
│   - Replace torch imports with mindspore                      │
│   - Use layers_compat for version-aware operations            │
│   - Update attention processors                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Model Migration                                        │
│   - Convert nn.Module to nn.Cell                              │
│   - Update forward() to construct()                           │
│   - Fix torch-specific operations                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Weight Conversion                                     │
│   - Extract HF weights                                        │
│   - Map to MindSpore format                                   │
│   - Save as safetensors                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Testing & Validation                                  │
│   - Test inference output                                     │
│   - Compare numerical accuracy                                │
│   - Benchmark performance                                     │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Analyze Source Model

### 1.1 Identify Pipeline Components

Create an inventory of all components:

```python
# Example analysis checklist
components = {
    "model_type": "UNet2DConditionModel / FluxTransformer2DModel / Custom",
    "text_encoder": ["CLIPTextModel", "T5EncoderModel", ...],
    "vae": "AutoencoderKL / CustomVAE",
    "scheduler": "DDIMScheduler / FlowMatchScheduler / Custom",
    "control_net": "ControlNetModel / None",
    "adapters": ["LoRA", "IP-Adapter", "T2I-Adapter"],
    "attention_type": "Standard / Flash / Custom",
}

# Check if similar architecture exists in mindone.diffusers
# See official SUPPORT_LIST.md for support status:
# https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md
```

### 1.3 Review HF Pipeline Structure

```python
# HF pipeline structure (example)
from diffusers import StableDiffusionPipeline

pipeline = StableDiffusionPipeline(
    vae=vae,
    text_encoder=text_encoder,
    tokenizer=tokenizer,
    unet=unet,
    scheduler=scheduler,
    safety_checker=None,
    feature_extractor=None,
)
```

## Step 2: Import Mapping

### 2.1 Basic Imports Transformation

| HF (PyTorch) | MindOne (MindSpore) |
|--------------|---------------------|
| `import torch` | `import mindspore as ms` |
| `import torch.nn as nn` | `from mindspore import nn` |
| `import torch.nn.functional as F` | `from mindspore import ops, mint` |
| `from torch import Tensor` | `ms.Tensor` |

### 2.2 Layer Imports

```python
# HF
from torch.nn import Linear, Conv2d, GroupNorm

# MindOne (use layers_compat for version compatibility)
from diffusers.models.layers_compat import group_norm
# Note: Conv2d and GroupNorm use native MindSpore

# Linear is called Dense in MindSpore Layer_std
from diffusers.models.layers_std import Linear
```

### 2.3 Attention Processor Imports

```python
# HF
from diffusers.models.attention_processor import (
    AttnProcessor2_0,
    FusedAttnProcessor2_0,
)

# MindOne
from diffusers.models.attention_processor import (
    AttnProcessor2_0,
    # Note: FusedAttnProcessor2_0 uses MindSpore native
)

# Use layers_compat for scaled_dot_product_attention
from diffusers.models.layers_compat import scaled_dot_product_attention
```

### 2.4 Utility Imports

```python
# HF
from diffusers.utils.torch_utils import randn_tensor
from torch.utils.checkpoint import checkpoint

# MindOne
from diffusers.utils.mindspore_utils import randn_tensor
from mindspore import ops
```

## Step 3: Model Migration

### 3.1 Module Base Class Conversion

```python
# HF Diffusers
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 64, 3)

    def forward(self, x):
        return self.conv(x)

# MindOne Diffusers
from mindspore import nn

class MyModel(nn.Cell):  # nn.Cell instead of nn.Module
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 64, 3)  # Same API

    def construct(self, x):  # construct instead of forward
        return self.conv(x)
```

### 3.2 Attention Implementation Migration

```python
# HF - Using PyTorch's SDPA
def hf_attention(query, key, value, mask=None):
    import torch.nn.functional as F
    return F.scaled_dot_product_attention(
        query, key, value,
        attn_mask=mask,
        dropout_p=0.0
    )

# MindOne - Using layers_compat
from diffusers.models.layers_compat import scaled_dot_product_attention

def mindone_attention(query, key, value, mask=None):
    return scaled_dot_product_attention(
        query, key, value,
        attn_mask=mask,
        dropout_p=0.0
    )
```

### 3.3 ConvTranspose2D Migration

```python
# HF
import torch.nn.functional as F
output = F.conv_transpose2d(
    input, weight, bias,
    stride=2, padding=1
)

# MindOne - Use layers_compat
from diffusers.models.layers_compat import conv_transpose2d
output = conv_transpose2d(
    input, weight, bias,
    stride=2, padding=1
)
```

### 3.4 Interpolate Migration

```python
# HF
import torch.nn.functional as F
output = F.interpolate(
    x, size=(H, W),
    mode='bilinear',
    align_corners=False
)

# MindOne - Use layers_compat
from diffusers.models.layers_compat import interpolate
output = interpolate(
    x, size=(H, W),
    mode='bilinear',
    align_corners=False
)
```

## Step 4: Weight Conversion

### 4.1 Extract HF Weights

```python
# HF Diffusers
from diffusers import StableDiffusionPipeline

pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

# Save components separately
pipeline.unet.save_pretrained("./hf_weights/unet")
pipeline.vae.save_pretrained("./hf_weights/vae")
pipeline.text_encoder.save_pretrained("./hf_weights/text_encoder")
```

### 4.2 Convert to MindSpore Format

```python
import mindspore as ms
import torch
from transformers import AutoModel

# Load HF model
hf_model = AutoModel.from_pretrained("model_id")
state_dict = hf_model.state_dict()

# Convert to MindSpore parameters
ms_state_dict = {}
for name, param in state_dict.items():
    ms_tensor = ms.Tensor(param.numpy())
    ms_state_dict[name] = ms.Parameter(ms_tensor, name=name)

# Save as safetensors (MindSpore version)
from mindone.safetensors.mindspore import save_file
save_file(ms_state_dict, "./mindspore_weights/model.safetensors")
```

### 4.3 Weight Name Mapping

For new architectures, you may need to map weight names:

```python
weight_mapping = {
    # HF name -> MindSpore name
    "model.layers.*.self_attention.query": "transformer.layers.*.attn.q_proj",
    "model.layers.*.self_attention.key": "transformer.layers.*.attn.k_proj",
    # Add more mappings as needed
}

def map_weight_state_dict(hf_sd, mapping):
    ms_sd = {}
    for hf_key, value in hf_sd.items():
        for pattern, ms_pattern in mapping.items():
            if pattern.replace("*", "") in hf_key:
                ms_key = hf_key.replace(pattern.replace("*", ""), ms_pattern.replace("*", ""))
                ms_sd[ms_key] = ms.Tensor(value.numpy())
    return ms_sd
```

## Step 5: Testing & Validation

### 5.1 Numerical Accuracy Check

```python
import numpy as np

def compare_outputs(hf_output, ms_output, rtol=1e-3, atol=1e-3):
    """
    Compare HF and MindSpore outputs for numerical equivalence.
    """
    hf_np = hf_output if isinstance(hf_output, np.ndarray) else hf_output.numpy()
    ms_np = ms_output if isinstance(ms_output, np.ndarray) else ms_output.asnumpy()

    # Ensure same shape
    assert hf_np.shape == ms_np.shape, f"Shape mismatch: {hf_np.shape} vs {ms_np.shape}"

    # Calculate relative difference
    max_diff = np.max(np.abs(hf_np - ms_np))
    relative_diff = max_diff / (np.max(np.abs(hf_np)) + 1e-8)

    print(f"Max absolute difference: {max_diff}")
    print(f"Max relative difference: {relative_diff}")

    if np.allclose(hf_np, ms_np, rtol=rtol, atol=atol):
        print("✓ Outputs match within tolerance")
        return True
    else:
        print("✗ Outputs differ significantly")
        return False
```

### 5.2 Inference Test

```python
import torch
import mindspore as ms

# Set same random seed for comparison
torch.manual_seed(42)
ms.set_seed(42)

# HF inference
hf_pipeline = StableDiffusionPipeline.from_pretrained("model_id")
hf_image = hf_pipeline("A cat", num_inference_steps=20).images[0]

# Mindone inference
from diffusers import StableDiffusionPipeline as MSStableDiffusionPipeline
ms_pipeline = MSStableDiffusionPipeline.from_pretrained("converted_model_id")
ms_image = ms_pipeline("A cat", num_inference_steps=20).images[0]

# Compare
from PIL import ImageChops
diff = ImageChops.difference(hf_image, ms_image)
print(f"Image difference: {diff.getbbox()}")
```

### 5.3 Performance Benchmark

```python
import time

def benchmark_pipeline(pipeline, prompt, iterations=10):
    times = []
    for _ in range(iterations):
        start = time.time()
        _ = pipeline(prompt)
        times.append(time.time() - start)

    avg_time = np.mean(times)
    std_time = np.std(times)
    print(f"Average time: {avg_time:.2f}s ± {std_time:.2f}s")
    return avg_time

# Benchmark HF
hf_time = benchmark_pipeline(hf_pipeline, "A cat")

# Benchmark MindSpore
ms_time = benchmark_pipeline(ms_pipeline, "A cat")

print(f"Performance ratio: {hf_time / ms_time:.2f}x")
```

## Common Migration Issues

### Issue 1: dim vs axis

```python
# HF (PyTorch)
x.mean(dim=1)  # or dim=(1,2)

# MindOne (MindSpore)
x.mean(axis=1)  # or axis=(1,2)
```

### Issue 2: Tensor device

```python
# HF - Explicit device placement
x = x.to('cuda')
model.to('cuda')

# MindOne - Device is implicit
ms.set_context(device_target="Ascend")
# No need to explicitly move tensors
```

### Issue 3: .numpy() vs .asnumpy()

```python
# HF
numpy_array = tensor.numpy()

# MindOne
numpy_array = tensor.asnumpy()
```

### Issue 4: View vs Reshape

```python
# HF - Can use .view()
new_tensor = tensor.view(...)

# MindOne - Use .reshape()
new_tensor = tensor.reshape(...)
```

### Issue 5: F.pad interpolation parameters

```python
# HF - pad parameter order
F.pad(x, [left, right, top, bottom])

# MindOne - pad parameter rename
from diffusers.models.layers_compat import pad
output = pad(x, (left, right, top, bottom), mode='constant')
```

## Checklist

Before claiming a pipeline is migrated:

- [ ] All torch imports replaced with mindspore
- [ ] nn.Module converted to nn.Cell
- [ ] forward() renamed to construct()
- [ ] Attention uses layers_compat.scaled_dot_product_attention
- [ ] ConvTranspose uses layers_compat.conv_transpose2d
- [ ] Interpolate uses layers_compat.interpolate
- [ ] Tensor operations use axis instead of dim
- [ ] .numpy() replaced with .asnumpy()
- [ ] Weights converted and saved
- [ ] Inference output matches HF within tolerance
- [ ] Performance is acceptable
- [ ] Documentation updated
- [ ] Tested on target hardware (Ascend)

## References

- [Architecture Overview](01-architecture-overview.md)
- [API Mapping Reference](02-api-mapping.md)
- [Folder Structure Differences](03-folder-structure.md)
- [Model Architecture Differences](04-model-architecture.md)
- [MindOne-Specific Components](05-mindone-specific.md)