# MindOne-Specific Components

This document describes components that are unique to mindone.diffusers or differ significantly from the HuggingFace version.

## Context Parallelism

**Location:** `hooks/context_parallel.py`

Context parallelism is a MindOne-specific feature for distributing large models across multiple devices by splitting the input sequence dimension.

### Key Classes

```python
class ContextParallelConfig:
    """Configuration for context parallel training"""
    def __init__(self, dp_group, cp_group, sp_group=None):
        self._mesh = DeviceMesh("cuda", (dp_size, cp_size), ("dp", "cp"))
        self._flattened_mesh = self._mesh._flatten()

class ContextParallelInput:
    """Spec for how input should be split for CP"""
    def __init__(self, split_dim, expected_dims, split_output=False):
        self.split_dim = split_dim
        self.expected_dims = expected_dims
        self.split_output = split_output

class ContextParallelOutput:
    """Spec for how output should be gathered from CP"""
    def __init__(self, gather_dim, expected_dims):
        self.gather_dim = gather_dim
        self.expected_dims = expected_dims
```

### Usage Example

```python
from diffusers.hooks.context_parallel import (
    ContextParallelConfig,
    ContextParallelInput,
    apply_context_parallel,
)

# Define CP config
parallel_config = ContextParallelConfig(dp_group, cp_group)

# Define how to split/gather tensors
plan = {
    "model.layers.0": {
        "hidden_states": ContextParallelInput(
            split_dim=1,
            expected_dims=4,
            split_output=False
        )
    },
    "model.layers.-1": Context_parallelOutput(
        gather_dim=1,
        expected_dims=4
    )
}

# Apply to model
apply_context_parallel(model, parallel_config, plan)
```

## MindSpore Utilities

**Location:** `utils/mindspore_utils.py`

### dtype Helper Functions

```python
def dtype_to_min(dtype):
    """Get minimum value for a dtype"""
    # Returns type-specific minimum values

def dtype_to_max(dtype):
    """Get maximum value for a dtype"""

def dtype_to_eps(dtype):
    """Get epsilon value for a dtype"""
```

### Tensor Creation

```python
import mindspore as ms
from diffusers.utils.mindspore_utils import randn_tensor

# MindSpore-compatible random tensor generation
x = randn_tensor(
    shape=(B, C, H, W),
    dtype=ms.float32,
    device=None  # device is implicit in MindSpore
)
```

### State Dict Handling

```python
def get_state_dict(model):
    """MindSpore version of getting model state dict"""
    # Returns parameters as a dictionary

def set_all_layers_trainable(model, trainable=True):
    """Set trainability of all layers"""
```

### Context Managers

```python
@contextmanager
def pynative_context(func):
    """Run function in pynative (eager) mode"""
    with ms.set_context(mode=ms.PYNATIVE_MODE):
        yield func
```

## Hook System Enhancements

**Location:** `hooks/` directory

MindOne extends the hook system with MindSpore-specific implementations:

### HookRegistry

```python
class HookRegistry:
    """Registry for model hooks in MindSpore"""
    def __init__(self):
        self._hooks: Dict[str, List[ModelHook]] = {}

    def register_hook(self, hook: ModelHook, hook_name: str):
        ...

    def remove_hook(self, hook_name: str):
        ...
```

### Pre- and Post-Construct Hooks

MindSpore uses `pre_construct` and `post_construct` instead of `pre_forward` and `post_forward`:

```python
class MyHook(ModelHook):
    def pre_construct(self, module, *args, **kwargs):
        # Called before construct()
        ...

    def post_construct(self, module, output):
        # Called after construct()
        ...
```

### Helper Utilities

**Location:** `hooks/_helpers.py`

```python
class AttentionProcessorMetadata:
    skip_processor_output_fn: Callable[[Any], Any]

class TransformerBlockMetadata:
    return_hidden_states_index: int = None
    return_encoder_hidden_states_index: int = None
```

## Modular Pipeline Architecture

### QwenImage Modular Pipeline

**Location:** `modular_pipelines/qwenimage/`

MindOne introduces a modular pipeline architecture for QwenImage that separates components:

```python
from diffusers.modular_pipelines import (
    QwenImageModularPipeline,
    QwenImageAutoBlocks,
    ComponentsManager,
    ComponentSpec,
)

# Define components
components = ComponentsManager()

# Add specifications
components.add_spec(
    "text_encoder",
    ComponentSpec(
        module= transformers.AutoModel,
        config= text_encoder_config
    )
)

# Build pipeline
pipeline = QwenImageModularPipeline(
    components=components,
    blocks=QwenImageAutoBlocks()
)
```

### Flux Modular Pipeline

```python
from diffusers.modular_pipelines import (
    FluxModularPipeline,
    FluxAutoBlocks,
)

# Modular pipeline for Flux models
pipeline = FluxModularPipeline(
    components=components,
    blocks=FluxAutoBlocks()
)
```

## New Models

### Flux2 Transformer

**Location:** `models/transformers/transformer_flux2.py`

```python
from diffusers import Flux2Transformer2DModel

model = Flux2Transformer2DModel(
    # Flux2-specific parameters
)
```

### Bria Transformer

**Location:** `models/transformers/transformer_bria.py`

```python
from diffusers import BriaTransformer2DModel

model = BriaTransformer2DModel(...)
```

### Kandinsky5 Transformer

**Location:** `models/transformers/transformer_kandinsky.py`

```python
from diffusers import Kandinsky5Transformer3DModel

model = Kandinsky5Transformer3DModel(...)
```

### QwenImage Components

* Transformer: `models/transformers/transformer_qwenimage.py`
* ControlNet: `models/controlnets/controlnet_qwenimage.py`
* VAE: `models/autoencoders/autoencoder_kl_qwenimage.py`

## New Pipelines

### Flux2 Pipeline

```python
from diffusers import Flux2Pipeline, Flux2ModularPipeline

# Standard pipeline
pipeline = Flux2Pipeline.pretrained(model_id)

# Modular pipeline
pipeline = Flux2ModularPipeline.from_pretrained(model_id)
```

### Bria Pipeline

```python
from diffusers import BriaPipeline

pipeline = BriaPipeline.from_pretrained("briaai/BRIA-2.0")
```

### Lucy Edit Pipeline

```python
from diffusers import LucyEditPipeline

pipeline = LucyEditPipeline.from_pretrained(
    "lucyedit/LucyEdit-V"
)
```

## Weight Saving Format

MindOne uses `mindone.safetensors.mindspore` for saving models:

```python
from mindone.safetensors.mindspore import save_file

save_file(
    weights_dict,
    "path/to/model.safetensors"
)
```

This is MindSpore's implementation of the safetensors format.

## Graph Mode vs Eager Mode

MindSpore has two execution modes:

```python
import mindspore as ms

# Graph mode (default for production, faster)
ms.set_context(mode=ms.GRAPH_MODE)

# PYNative mode (eager, better for debugging)
ms.set_context(mode=ms.PYNATIVE_MODE)
```

MindOne often uses `pynative_context` for specific operations that don't work well in graph mode.

## Support List

**Location:** Official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) in mindone repository

MindOne provides a comprehensive support matrix showing which pipelines are:

- Fully supported
- Preview support (experimental)
- Not yet ported

```markdown
| Model | Status | Notes |
|-------|--------|-------|
| Stable Diffusion | Full | ✅ |
| SDXL | Full | ✅ |
| SD3 | Full | ✅ |
| Flux | Full | ✅ |
| Flux2 | Preview | Preview of latest HF diffusers support |
```

## License and Attribution

MindOne diffusers maintains the same Apache 2.0 license as HF diffusers, with attribution noted in source files:

```python
# This code is adapted from https://github.com/huggingface/diffusers
# with modifications to run diffusers on mindspore.
```

## Summary

MindOne-specific components enable:

1. **Context Parallelism** - Distributed training for large sequences
2. **MindSpore Utilities** - Framework-specific helper functions
3. **Hook System** - Training time optimizations
4. **Modular Pipelines** - Composable architecture for new models
5. **New Models** - Flux2, Bria, Kandinsky5, QwenImage
6. **Graph Mode Optimization** - Production-ready compilation