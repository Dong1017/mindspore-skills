# API Mapping Reference: PyTorch to MindSpore

This document provides a comprehensive mapping of PyTorch APIs to MindSpore APIs as used in HF diffusers vs mindone.diffusers.

## Core Framework Imports

### Basic Imports

| PyTorch (HF) | MindSpore (MindOne) | Usage |
|--------------|---------------------|-------|
| `import torch` | `import mindspore as ms` | Main framework |
| `import torch.nn as nn` | `from mindspore import nn` | Neural network modules |
| `import torch.nn.functional as F` | `from mindspore import ops` / `from mindspore import mint` | Functional operations |
| `from torch import Tensor` | `ms.Tensor` | Tensor type annotation |

**MindSpore Specific Notes:**
- `mint` is the MindSpore tensor prefix module, similar to `torch`
- `ops` contains functional operations
- `nn` contains neural network layers

## Layer/Layer Compatibility

### Linear Layers

```python
# PyTorch
torch.nn.Linear(in_features, out_features, bias=True)
```

```python
# MindSpore (via layers_compat.py)
nn.Dense(in_features, out_features, has_bias=True)
# Custom layer_std provides standardized naming: Linear
```

### Convolution Layers

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `nn.Conv2d(in_ch, out_ch, kernel, stride, padding)` | `nn.Conv2d(in_ch, out_ch, kernel_size, stride, pad_mode='pad', padding=padding)` | Note `pad_mode='pad'` and explicit padding |
| `nn.ConvTranspose2d(...)` | `nn.Conv2dTranspose(...)` | Different naming |

### Normalization Layers

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `nn.GroupNorm(num_groups, num_channels)` | `nn.GroupNorm(num_groups, num_channels)` | Same signature |
| `nn.LayerNorm(normalized_shape)` | `nn.LayerNorm(normalized_shape, eps=1e-5)` | eps differs (PyTorch: 1e-5) |
| `nn.BatchNorm2d(...)` | `nn.BatchNorm2d(...)` | Same |

### Activation Functions

| PyTorch | MindSpore | Mint (functional) |
|---------|-----------|-------------------|
| `nn.SiLU()` | `nn.SiLU()` | `mint.nn.functional.silu()` |
| `nn.GELU()` | `nn.GELU()` | `mint.nn.functional.gelu()` |
| `nn.ReLU()` | `nn.ReLU()` | `mint.nn.functional.relu()` |
| `F.silu(x)` | `ops.sigmoid(x) * x` or `ops.erf()` based | Use ops implementation |

## Tensor Operations

### Tensor Creation

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `torch.randn(*size)` | `ms.ops.randn(*size)` or `ms.Tensor(...)` | Use `randn_tensor()` utility |
| `torch.zeros(*size)` | `ms.ops.zeros(*size)` | Same |
| `torch.ones(*size)` | `ms.ops.ones(*size)` | Same |
| `torch.empty(*size)` | `ms.Tensor(shape, dtype)` | Different approach |
| `torch.from_numpy(arr)` | `ms.Tensor(arr)` | Same concept |
| `tensor.numpy()` | `tensor.asnumpy()` | Different method name |

### Tensor Manipulation

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `x.reshape(shape)` | `x.reshape(shape)` | Same |
| `x.view(shape)` | `x.reshape(shape)` | MindSpore uses reshape |
| `x.permute(*dims)` | `x.transpose(*dims)` | Different name |
| `x.transpose(dim0, dim1)` | `x.transpose(dim0, dim1)` | Same |
| `x.mean(dim)` | `x.mean(axis=dim)` | axis vs dim |
| `x.sum(dim)` | `x.sum(axis=dim)` | axis vs dim |
| `x.cat(tensors, dim)` | `ops.Concat(axis=dim)(tensors)` | Different API |
| `x.stack(tensors, dim)` | `ops.Stack(axis=dim)(tensors)` | Different API |
| `x.clamp(min, max)` | `ops.clip_by_value(x, min, max)` | Different API |
| `x.chunk(chunks, dim)` | `ops.chunk(x, chunks, axis=dim)` | Differences |
| `x.split(split_size, dim)` | `ops.split(x, split_size, axis=dim)` | Differences |

### Mathematical Operations

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `torch.matmul(a, b)` | `ops.matmul(a, b)` | Same |
| `torch.dot(a, b)` | `ops.dot(a, b)` | Same |
| `torch.bmm(a, b)` | `ops.batch_matmul(a, b)` | Different name |
| `torch.einsum(eq, *args)` | `ops.einsum(eq, *args)` | Same |
| `torch.softmax(x, dim)` | `ops.softmax(x, axis=dim)` | axis vs dim |
| `torch.sigmoid(x)` | `ops.sigmoid(x)` | Same |
| `torch.tanh(x)` | `ops.tanh(x)` | Same |
| `torch.sin(x)` | `ops.sin(x)` | Same |
| `torch.cos(x)` | `ops.cos(x)` | Same |

### Comparison Operations

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `x == y` | `x == y` | Same |
| `torch.eq(x, y)` | `ops.equal(x, y)` | Different name |
| `torch.where(cond, x, y)` | `ops.select(cond, x, y)` | Different name |
| `x.gather(dim, index)` | `ops.gather_d(x, dim, index)` | Different API |

## Attention Operations

### Scale Dot Product Attention

```python
# PyTorch (FusedAttnProcessor2_0)
torch.nn.functional.scaled_dot_product_attention(
    query, key, value,
    attn_mask=attn_mask,
    dropout_p=dropout,
    is_causal=is_causal
)
```

```python
# MindSpore
import mindspore.ops as ops
import mindspore.nn as nn

# Using MindSpore's attention implementation
ops.FlashAttentionScore(
    query, key, value,
    attention_mask=attn_mask,
    dropout_rate=dropout,
    # Note: MindSpore has different parameter names
)
```

### Multiplication/Rotary Embeddings

```python
# PyTorch
x @ y  # Matrix multiplication

# MindSpore
mint.matmul(x, y)  # Matrix multiplication
```

## Random Operations

```python
# PyTorch
torch.manual_seed(seed)
torch.nn.init.normal_(tensor, mean, std)
torch.nn.init.xavier_uniform_(tensor)

# MindSpore
ms.set_seed(seed)
nn.init.Normal(mean, std)(tensor)
nn.init.XavierUniform()(tensor)
```

## Distributed Operations

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `torch.distributed.all_gather(...)` | `ops.AllGather(...)` | Different import path |
| `torch.distributed.all_reduce(...)` | `ops.AllReduce(...)` | Different import path |
| `torch.distributed.get_rank()` | `ops.get_rank()` | Different path |

## Gradient Operations

```python
# PyTorch
x.requires_grad_(True)
loss.backward()
torch.autograd.grad(loss, inputs)

# MindSpore
# MindSpore uses automatic differentiation differently
# with value_and_grad mechanism
```

## Device Operations

```python
# PyTorch
x.to(device)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x.cuda()

# MindSpore
# MindSpore uses a different compute graph approach
# Device placement is handled by the framework
ms.set_context(device_target="Ascend")  
```

## Type Casting

| PyTorch | MindSpore | Notes |
|---------|-----------|-------|
| `x.float()` | `x.float()` | Same constant name |
| `x.half()` | `x.half()` | Same constant name |
| `x.bfloat16()` | `x.bfloat16()` | Same constant name |
| `x.int()` | `x.int()` | Same constant name |
| `x.long()` | `x.long()` | Same constant name |

## Data Types

| PyTorch | MindSpore |
|---------|-----------|
| `torch.float32` | `ms.float32` |
| `torch.float16` | `ms.float16` |
| `torch.bfloat16` | `ms.bfloat16` |
| `torch.int32` | `ms.int32` |
| `torch.int64` | `ms.int64` |
| `torch.uint8` | `ms.uint8` |
| `torch.bool` | `ms.bool_` |

## Model-Specific Differences

### UNet2DConditionModel

```python
# HF diffusers
from diffusers import UNet2DConditionModel
model = UNet2DConditionModel(...)
x = model(sample, timestep, encoder_hidden_states)

# MindOne diffusers
from diffusers import UNet2DConditionModel
model = UNet2DConditionModel(...)
x = model(sample, timestep, encoder_hidden_states)
# Same API, different internal implementation
```

### Output Types

```python
# Both use the same dataclass structure with ms.Tensor vs torch.Tensor
@dataclass
class UNet2DConditionOutput(BaseOutput):
    sample: Union[ms.Tensor, np.ndarray]  # MindSpore uses ms.Tensor
    # sample: torch.Tensor  # PyTorch version
```

## Utility Functions

### Random Tensor Generation

MindOne provides custom utility in `utils/mindspore_utils.py`:

```python
# MindSpore version of torch.randn
def randn_tensor(
    shape,
    generator=None,
    device=None,
    dtype=None,
    layout=None,
):
    """
    Creates a tensor with random normal distribution.
    MindSpore port of torch.randn.
    """
    # Implementation uses MindSpore ops
    ...
```

## Summary: Key Migration Patterns

1. **Replace `torch` with `ms`** for basic operations
2. **Replace `dim` with `axis`** in reduction operations
3. **Use `ops` module** for functional operations
4. **Replace `.numpy()` with `.asnumpy()`**
5. **MindSpore works with compute graphs** - eager mode vs graph mode differences
6. **Device placement is implicit** in MindSpore vs explicit `.to(device)` in PyTorch
7. **Attention mechanisms** may use different implementations (e.g., `FusedAttnProcessor2_0` vs MindSpore native)

See also:
- [`mindone/diffusers/models/layers_compat.py`](../../../../mindone/mindone/diffusers/models/layers_compat.py) - Detailed layer compatibility layer
- [`mindone/diffusers/utils/mindspore_utils.py`](../../../../mindone/mindone/diffusers/utils/mindspore_utils.py) - MindSpore-specific utilities

## Special Operations in layers_compat.py

The `layers_compat.py` module provides compatibility implementations for MindSpore operations that may not be available in all versions. Key operators include:

### Convolution Transpose

```python
# layers_compat.py provides version-aware implementations
from mindone.diffusers.models.layers_compat import conv_transpose1d, conv_transpose2d, conv_transpose3d

# Usage - looks like F.conv_transpose2d but works with MindSpore
output = conv_transpose2d(input, weight, bias=bias, stride=2, padding=1)
```

**Version support:**
- `conv_transpose2d`: Native for MindSpore >= 2.3.0, custom otherwise
- `conv_transpose1d`, `conv_transpose3d`: Always custom implementation

### Group Norm

```python
from mindone.diffusers.models.layers_compat import group_norm

# Equivalent to torch.nn.functional.group_norm
output = group_norm(x, num_groups, weight, bias, eps)
```

**Version support:** Native for MindSpore >= 2.3.0, custom otherwise

### Interpolate

```python
from mindone.diffusers.models.layers_compat import interpolate, upsample_nearest3d_free_interpolate

# Standard interpolate
output = interpolate(x, size=(H, W, T), mode='nearest')

# Special 3D version (bypasses slow Ascend operator)
output = upsample_nearest3d_free_interpolate(x, size=(T, H, W), mode='nearest')
```

**Special case:** `upsample_nearest3d_free_interpolate` uses optimized decomposition for 3D nearest neighbor upsampling on Ascend hardware.

### Scaled Dot Product Attention

```python
from mindone.diffusers.models.layers_compat import scaled_dot_product_attention

# Equivalent to F.scaled_dot_product_attention
output = scaled_dot_product_attention(
    query, key, value,
    attn_mask=attn_mask,
    dropout_p=0.0,
    is_causal=False,
    backend="flash"  # or "math"
)
```

**Features:**
- Supports both flash attention and math-based implementation
- Handles attention mask conversion between PyTorch and MindSpore conventions
- Supports Grouped Query Attention (GQA)

### Other Operations

| Operation | Purpose | Notes |
|-----------|---------|-------|
| `multinomial` | Sampling from multinomial distribution | Native for MindSpore >= 2.4.1 |
| `pad` | Tensor padding | Supports constant, replicate, reflect modes |
| `view_as_complex` | View last 2 dims as complex | Always custom |
| `unflatten` | Unflatten a tensor dimension | Always custom |
| `RMSNorm` | Root Mean Square Normalization | Always custom |
| `DeviceMesh` | Device mesh for distributed training | Always custom |
| `cartesian_prod` | Cartesian product of tensors | Always custom |

### AMP Strategy

```python
from mindone.diffusers.models.layers_compat import set_amp_strategy, AmpLevel

# Apply mixed precision strategy
set_amp_strategy(
    net,
    weight_dtype=ms.float16,
    level=AmpLevel.AmpO3,
    white_list=[],  # Layers to skip casting
    black_list=[]  # Layers to explicitly cast
)
```

## Comprehensive API Mapping Reference

For a complete and detailed PyTorch to MindSpore API mapping table maintained by the MindSpore community, see:

- **[pytorch_api_mapping.md](api_mapping/pytorch_api_mapping.md)** - Comprehensive API mapping table covering:
  - General difference parameters (e.g., `out`, `device`, `requires_grad`, etc.)
  - torch.* namespace APIs (abs, acos, add, all, any, argmax, etc.)
  - torch.nn.* modules (Linear, Conv2d, BatchNorm, etc.)
  - torch.nn.functional.* APIs (dropout, softmax, convolutions, etc.)
  - torch.optim optimizers
  - torch.distributed operations
  - Data type and device handling

This document is maintained by the MindSpore community and provides detailed information about:
- API consistency criteria and exceptions
- Parameter differences between PyTorch and MindSpore
- Input/output data type support ranges
- Behavior differences in specific scenarios

**External Source:** [MindSpore Documentation - PyTorch API Mapping](https://www.mindspore.cn/docs/en/master/note/api_mapping/pytorch_api_mapping.html)

## Gradient Checkpointing / Recompute

Gradient checkpointing is used in diffusers models to reduce memory usage during training. PyTorch and MindSpore have different implementations:

| PyTorch | MindSpore |
|---------|-----------|
| `torch.utils.checkpoint.checkpoint(function)` | `mindspore.nn.Cell.recompute()` |
| Function wrapper | Cell method wrapper |

### PyTorch

```python
from torch.utils.checkpoint import checkpoint as cp
import torch.nn as nn

class Net(nn.Module):
    def forward(self, x):
        x = nn.functional.relu(self.fc1(x))
        x = cp(self._checkpoint, x)  # Wrap for checkpoint
        x = self.fc3(x)
        return x

    def _checkpoint(self, x):
        x = nn.functional.relu(self.fc2(x))
        return x
```

### MindSpore

```python
from mindspore import nn, ops

class Net(nn.Cell):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Dense(12, 24)
        self.fc2 = nn.Dense(24, 48)
        self.fc2.recompute()  # Mark for recomputation
        self.fc3 = nn.Dense(48, 2)

    def construct(self, x):
        x = self.fc1(x)
        x = self.fc2(x)  # Will be recomputed during backward
        x = self.fc3(x)
        return x
```

**Key Differences:**
- PyTorch uses function wrapping with `checkpoint()` wrapper
- MindSpore uses `.recompute()` method on Cells/operations
- PyTorch: `preserve_rng_state` parameter for RNG state
- MindSpore: `mp_comm_recompute`, `parallel_optimizer_comm_recompute` for parallel scenarios

**See also:** [checkpoint_diff.md](api_mapping/checkpoint_diff.md) - Detailed documentation about gradient checkpointing differences