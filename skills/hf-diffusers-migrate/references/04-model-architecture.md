# Model Architecture Differences

This document details the specific differences in model architecture implementations between HF diffusers and mindone.diffusers.

## ModelMixin and Framework Integration

### HF Diffusers (PyTorch-based)

```python
from diffusers.models.modeling_utils import ModelMixin

class MyModel(ModelMixin):
    def __init__(self, ...):
        super().__init__()
        self.conv = nn.Conv2d(...)
        self.linear = nn.Linear(...)

    # PyTorch forward
    def forward(self, x):
        return self.linear(self.conv(x))
```

### MindOne Diffusers (MindSpore-based)

```python
from diffusers.models.modeling_utils import ModelMixin

class MyModel(ModelMixin):
    def __init__(self, ...):
        super().__init__()
        self.conv = nn.Conv2d(...)  # MindSpore Conv2d
        self.linear = nn.Dense(...)  # MindSpore Dense instead of Linear

    # MindSpore construct (instead of forward)
    def construct(self, x):
        return self.linear(self.conv(x))
```

**Key Difference:** MindSpore uses `construct()` instead of `forward()` for the computation method.

## UNet2DConditionModel Comparison

### Imports and Base Classes

**HF Version:**
```python
import torch
import torch.nn as nn
from ...loaders import PeftAdapterMixin, UNet2DConditionLoadersMixin
from ...loaders.single_file_model import FromOriginalModelMixin
from ..attention_processor import (
    FusedAttnProcessor2_0,  # PyTorch flash attention
    ...
)

class UNet2DConditionModel(
    ModelMixin, ConfigMixin, FromOriginalModelMixin,
    UNet2DConditionLoadersMixin, PeftAdapterMixin
):
```

**MindOne Version:**
```python
import mindspore as ms
from mindspore import mint, nn, ops  # Note: mint instead of torch
from ...loaders import PeftAdapterMixin, UNet2DConditionLoadersMixin
from ...loaders.single_file_model import FromOriginalModelMixin
from ..attention_processor import (
    # No FusedAttnProcessor2_0 in __init__
    # Uses MindSpore native attention
    ...
)

class UNet2DConditionModel(
    ModelMixin, ConfigMixin, FromOriginalModelMixin,
    UNet2DConditionLoadersMixin, PeftAdapterMixin
):
```

### Attention Module Differences

**HF (attention.py):**
```python
import torch
import torch.nn.functional as F
from torch.nn.functional import scaled_dot_product_attention

# Flash Attention for PyTorch
class FusedAttnProcessor2_0:
    def __call__(self, attn, hidden_states, ...):
        # Use PyTorch native SDPA
        batch_size, sequence_length, _ = hidden_states.shape
        query = attn.to_q(hidden_states)
        key = attn.to_k(hidden_states)
        value = attn.to_v(hidden_states)

        hidden_states = F.scaled_dot_product_attention(
            query, key, value,
            attn_mask=attention_mask,
            dropout_p=attn.dropout_p,
            is_causal=attn.is_causal
        )
```

**MindOne (attention.py):**
```python
import mindspore as ms
from mindspore import mint, nn, ops
from .layers_compat import scaled_dot_product_attention

# Uses layers_compat.scaled_dot_product_attention
class AttnProcessor2_0:
    def __call__(self, attn, hidden_states, ...):
        batch_size, sequence_length, _ = hidden_states.shape
        query = attn.to_q(hidden_states)
        key = attn.to_k(hidden_states)
        value = attn.to_v(hidden_states)

        # Use MindSpore compatible SDPA from layers_compat
        hidden_states = scaled_dot_product_attention(
            query, key, value,
            attn_mask=attention_mask,
            dropout_p=attn.dropout_p,
            is_causal=attn.is_causal
        )
```

### ResNet Block Comparison

**HF (resnet.py):**
```python
import torch
import torch.nn as nn

class ResnetBlock2D(nn.Module):
    def __init__(self, ...):
        super().__init__()
        self.norm1 = nn.GroupNorm(num_groups, channels)
        self.conv1 = nn.Conv2d(...)

    def forward(self, input_tensor, ...):
        # PyTorch normalization
        hidden_states = F.group_norm(...)
        hidden_states = self.conv1(hidden_states)
        # ...
        return output_tensor
```

**MindOne (resnet.py):**
```python
import mindspore as ms
from mindspore import nn, ops
from .layers_compat import group_norm  # Version-aware

class ResnetBlock2D(nn.Cell):  # nn.Cell instead of nn.Module
    def __init__(self, ...):
        super().__init__()
        self.norm1 = nn.GroupNorm(num_groups, channels)
        self.conv1 = nn.Conv2d(...)  # Same API

    def construct(self, input_tensor, ...):  # construct instead of forward
        # May use layers_compat.group_norm
        hidden_states = self.norm1(input_tensor)
        hidden_states = self.conv1(hidden_states)
        # ...
        return output_tensor
```

## Transformer Models

### Flux Transformer

**HF (transformer_flux.py):**
```python
import torch
import torch.nn as nn
from ...attention_processor import AttnProcessor2_0, FusedAttnProcessor2_0

class FluxTransformer2DModel(nn.Module):
    def __init__(self, ...):
        super().__init__()
        self.transformer_blocks = nn.ModuleList(...)

    def forward(self, hidden_states, ...):
        for block in self.transformer_blocks:
            hidden_states = block(hidden_states, ...)
    return hidden_states
```

**MindOne (transformer_flux.py):**
```python
import mindspore as ms
from mindspore import mint, nn, ops
from ...attention_processor import (
    AttnProcessor2_0,
    # No FusedAttnProcessor2_0, the MindSpore version handles this
)

class FluxTransformer2DModel(nn.Cell):  # nn.Cell
    def __init__(self, ...):
        super().__init__()
        self.transformer_blocks = nn.CellList(...)  # CellList instead of ModuleList

    def construct(self, hidden_states, ...):  # construct instead of forward
        for block in self.transformer_blocks:
            hidden_states = block(hidden_states, ...)
    return hidden_states
```

## Key Architecture Differences Summary

| Aspect | HF Diffusers | MindOne Diffusers |
|--------|--------------|-------------------|
| Base Module | `nn.Module` | `nn.Cell` |
| Forward Method | `forward()` | `construct()` |
| Module Lists | `nn.ModuleList` | `nn.CellList` |
| ParameterDict | `nn.ParameterDict` | NA |
| Linear Layer | `nn.Linear` | `mint.nn.Linear` |
| Conv Transpose 2D | `nn.ConvTranspose2d` | `mint.nn.ConvTranspose2d` |
| Group Norm | `nn.GroupNorm` or `F.group_norm` | `nn.GroupNorm` of `mint.nn.GroupNorm` |
| Attention | `F.scaled_dot_product_attention`, Flash Attention | `layers_compat.scaled_dot_product_attention()` |
| Interpolate | `F.interpolate()` | `layers_compat.interpolate()` |
| Pad | `F.pad()` | `layers_compat.pad()` |

## Output Type Differences

**Both use similar structure:**

```python
@dataclass
class UNet2DConditionOutput(BaseOutput):
    sample: Union[ms.Tensor, np.ndarray]  # MindSpore uses ms.Tensor
    # sample: torch.Tensor  # PyTorch version
```

The output dataclasses are similar, with mindone using `ms.Tensor` instead of `torch.Tensor`.

## Weight Initialization

**HF (torch.nn.init):**
```python
import torch.nn.init as init

def init_weights(self):
    init.kaiming_uniform_(self.weight.data)
    init.zeros_(self.bias.data)
```

**MindOne:**
```python
from mindspore import nn
from mindspore.common.initializer import initializer, HeUniform, Zero

def init_weights(self):
    # MindSpore uses initializer API
    self.weight.set_data(initializer(HeUniform(), self.weight.shape))
    self.bias.set_data(initializer(Zero(), self.bias.shape))
```

## Device Handling

**HF (PyTorch):**
```python
model = UNet2DConditionModel(...)
model.to('cuda')  # Explicit device placement
x = x.to('cuda')
```

**MindOne:**
```python
import mindspore as ms

# Set context for Graph mode, device is implicit
ms.set_context(mode=ms.GRAPH_MODE, device_target="Ascend")

model = UNet2DConditionModel(...)
# Device placement is handled by the framework
```

MindSpore uses a different compute model where device placement is managed by the framework's compilation strategy rather than explicit `.to(device)` calls.