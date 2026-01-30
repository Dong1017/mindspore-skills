# Architecture Overview

## High-Level Directory Structure

### HuggingFace Diffusers
```
src/diffusers/
├── commands/           # CLI commands
├── experimental/        # Experimental features
├── guiders/            # Guidance mechanisms (12 files)
├── hooks/              # Hook system (12 files)
├── image_processor/    # Image processing utilities
├── loaders/            # Model loading utilities
├── models/             # Model implementations
│   ├── autoencoders/   # VAE models (20 files)
│   ├── controlnets/    # ControlNet models (7 files)
│   ├── transformers/   # Transformer models (35 files)
│   └── unets/          # UNet models (17 files)
├── modular_pipelines/  # Modular pipeline components
│   ├── flux/
│   ├── stable_diffusion_xl/
│   └── wan/
├── pipelines/          # Pipeline implementations (100+ models)
├── quantizers/         # Quantization utilities
├── schedulers/         # Noise schedulers (45 files)
└── utils/              # Utility functions
```

### MindOne Diffusers
```
mindone/diffusers/
├── guiders/            # Guidance mechanisms (12 files)
├── hooks/              # Hook system (11 files) + context_parallel.py
├── image_processor/    # Image processing utilities
├── loaders/            # Model loading utilities
├── models/             # Model implementations
│   ├── autoencoders/   # VAE models (20 files) + autoencoder_kl_flux2.py
│   ├── controlnets/    # ControlNet models (7 files)
│   ├── transformers/   # Transformer models (38 files)
│   │   └── + transformer_flux2.py, transformer_bria.py, transformer_kandinsky.py
│   └── unets/          # UNet models (16 files)
│       └── - unet_2d_condition_flax.py, unet_2d_blocks_flax.py
├── modular_pipelines/  # Modular pipeline components
│   ├── flux/
│   ├── qwenimage/      # NEW - only in mindone
│   ├── stable_diffusion_xl/
│   └── wan/
├── pipelines/          # Pipeline implementations (100+ models)
├── schedulers/         # Noise schedulers (43 files)
├── utils/              # Utility functions
│   └── + mindspore_utils.py  # MindSpore-specific utilities

**Note:** Support status matrix is available at the official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) in the mindone repository.
```

## Key Architectural Differences

### 1. Framework Base

| Component | HF Diffusers | MindOne Diffusers |
|-----------|--------------|-------------------|
| Base Framework | PyTorch | MindSpore |
| Module Base | `torch.nn.Module` | `mindspore.nn.Cell` |
| Tensor Type | `torch.Tensor` | `ms.Tensor` |
| GPU Backend | CUDA | Ascend |

### 2. MindOne-Specific Features

#### A. Only in MindOne (not in HF):

1. **Context Parallelism** (`hooks/context_parallel.py`)
   - `ContextParallelConfig`
   - `ContextParallelInput`
   - `ContextParallelOutput`
   - `all_gather` for distributed training

2. **Additional Models**:
   - `AutoencoderKLFlux2`
   - `Flux2Transformer2DModel`
   - `BriaTransformer2DModel`
   - `QwenImageTransformer2DModel`
   - `Kandinsky5Transformer3DModel`

3. **Additional Pipelines**:
   - `Flux2Pipeline`
   - `Flux2ModularPipeline`
   - `BriaPipeline`
   - `QwenImageModularPipeline` (multiple variants)
   - `Kandinsky5T2VPipeline`

4. **MindSpore Utilities** (`utils/mindspore_utils.py`):
   - `dtype_to_min()`, `dtype_to_max()`, `dtype_to_eps()`
   - `randn_tensor()` - MindSpore version
   - `get_state_dict()` - MindSpore parameter handling
   - `pynative_context` - Context manager for eager mode

#### B. Only in HF (not in Mindone):

1. **Flax Support**:
   - `models/modeling_flax_utils.py`
   - `models/modeling_pytorch_flax_utils.py`
   - `models/vae_flax.py`
   - `models/autoencoders/vae_flax.py`
   - `models/controlnets/controlnet_flax.py`
   - `models/unets/unet_2d_condition_flax.py`
   - `schedulers/*_flax.py` files

2. **Additional Utilities**:
   - `utils/torch_utils.py` - PyTorch-specific utilities
   - `utils/accelerate_utils.py`
   - `utils/video_processor.py` (different implementation)
   - `utils/dummy_*` files for optional dependencies

3. **Experimental Directory**:
   - Experimental features not ported to MindOne

### 3. Shared Components (Identical Structure)

Both libraries have these components with highly similar structure:
- `guiders/` - Guidance mechanisms
- `hooks/` - Hook system (HF has more features)
- `loaders/` - Model loading
- `pipelines/` - Pipeline implementations
- `schedulers/` - Noise schedulers

### 4. Import Differences

HF Diffusers uses lazy imports with extensive dependency checks for optional packages.

MindOne Diffusers has simpler imports since it primarily targets MindSpore.

**Example Import Diff:**

```python
# HF Diffusers
import torch
from torch import nn, Tensor
from torch.utils.checkpoint import checkpoint

# MindOne Diffusers
import mindspore as ms
from mindspore import mint, nn, ops
from mindspore.nn.utils import no_init_parameters
from mindone.safetensors.mindspore import save_file as safe_save_file
```

## Files Size Comparison (based on directory listings)

| Category | HF Files | MindOne Files | Notes |
|----------|----------|---------------|-------|
| models/ | 37 files | 36 files | Similar count, different implementations |
| autoencoders/ | 20 files | 20 files | +1 in mindone (flux2) |
| transformers/ | 35 files | 38 files | +3 in mindone (flux2, bria, kandinsky) |
| unets/ | 17 files | 16 files | -2 Flax files in mindone |
| pipelines/ | 90+ | 85+ | Similar, minor differences |
| schedulers/ | 45 files | 43 files | -2 Flax schedulers in mindone |
| loaders/ | 12 files | 12 files | Nearly identical |
| hooks/ | 12 files | 11 files | +context_parallel in mindone |
| guiders/ | 12 files | 12 files | Nearly identical |