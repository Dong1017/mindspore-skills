# Folder Structure Differences

This document provides a detailed comparison of folder structures between HF diffusers and mindone.diffusers.

## Complete Directory Listing Comparison

### Root Level Files

| File | HF | MindOne | Notes |
|------|----|--------|----|
| `__init__.py` | ✓ | ✓ | Different exported modules |
| `version.py` | ✗ | ✗ | Version in `__init__.py` instead |
| `configuration_utils.py` | ✓ | ✓ | Same |
| `image_processor.py` | ✓ | ✓ | Same |
| `export_onnx.py` | ✓ | ✗ | Not in mindone |
| `optimization.py` | ✓ | ✓ | Same |

### Core Subdirectories - Side-by-Side

## `models/` Directory

### autoencoders/

| HF | MindOne | Difference |
|----|--------|-----------|
| autoencoder_dc.py | ✓ | ✓ |
| autoencoder_kl.py | ✓ | ✓ |
| autoencoder_kl_allegro.py | ✓ | ✓ |
| autoencoder_kl_cogvideox.py | ✓ | ✓ |
| autoencoder_kl_cosmos.py | ✓ | ✓ |
| autoencoder_kl_hunyuan_video.py | ✓ | ✓ |
| autoencoder_kl_ltx.py | ✓ | ✓ |
| autoencoder_kl_magvit.py | ✓ | ✓ |
| autoencoder_kl_mochi.py | ✓ | ✓ |
| autoencoder_kl_qwenimage.py | ✓ | ✓ |
| autoencoder_kl_temporal_decoder.py | ✓ | ✓ |
| autoencoder_kl_wan.py | ✓ | ✓ |
| autoencoder_oobleck.py | ✓ | ✓ |
| autoencoder_tiny.py | ✓ | ✓ |
| autoencoder_asym_kl.py | ✓ | ✓ |
| consistency_decoder_vae.py | ✓ | ✓ |
| vae.py | ✓ | ✓ |
| vq_model.py | ✓ | ✓ |
| **autoencoder_kl_flux2.py** | ✗ | ✓ | **NEW in MindOne only** |

### transformers/

| HF | MindOne | Status |
|----|--------|--------|
| *All 35 HF files* | ✓ | ✓ |
| **transformer_flux2.py** | ✗ | ✓ | NEW in MindOne |
| **transformer_bria.py** | ✗ | ✓ | NEW in MindOne |
| **transformer_kandinsky.py** | ✗ | ✓ | NEW in MindOne |

**Note:** All 35 HF transformer files exist in MindOne, plus 3 additional ones.

### unets/

| HF | MindOne | Status |
|----|--------|--------|
| *15 standard UNet files* | ✓ | ✓ |
| unet_2d_blocks.py | ✓ | ✓ |
| unet_3d_blocks.py | ✓ | ✓ |
| unet_2d_condition_flax.py | ✓ | ✗ | Removed in MindOne (Flax support) |
| unet_2d_blocks_flax.py | ✓ | ✗ | Removed in MindOne (Flax support) |

### controlnets/

| File | HF | MindOne |
|------|----|--------|
| controlnet.py | ✓ | ✓ |
| controlnet_epoch.py | ✓ | ✓ |
| controlnet_flux.py | ✓ | ✓ |
| controlnet_hunyuan.py | ✓ | ✓ |
| controlnet_sd3.py | ✓ | ✓ |
| controlnet_sana.py | ✓ | ✓ |
| controlnet_sparsectrl.py | ✓ | ✓ |
| controlnet_union.py | ✓ | ✓ |
| controlnet_xs.py | ✓ | ✓ |
| multicontrolnet.py | ✓ | ✓ |
| multicontrolnet_union.py | ✓ | ✓ |

## `pipelines/` Directory

MindOne has a similar structure with most HF pipelines. The main difference is the absence of Flax-specific pipelines.

### HF-only pipelines (not in MindOne):

- `flax_*.py` files (Flax-JAX support)
- `onnx_*.py` files (ONNX runtime support)

### MindOne-only pipelines (not in HF):

- Flux2 variants (`pipelines/flux/pipeline_flux2.py`)
- QwenImage variants (`pipelines/qwenimage/` directory with multiple pipelines).
- BriaPipeline (`pipelines/bria/pipeline_bria.py`)
- LucyEditPipeline (`pipelines/lucy_edit/pipeline_lucy_edit.py`)

## `schedulers/` Directory

| File | HF | MindOne | Notes |
|------|----|--------|-------|
| scheduler_config.py | ✓ | ✓ | Same |
| scheduling_* (45 files total) | ✓ | ✓ | Most schedulers common |
| Flax schedulers | ✓ | ✗ | Removed in MindOne |

## `loaders/` Directory

| File | HF | MindOne |
|------|----|--------|
| from_single_file.py | ✓ | ✓ |
| lora.py | ✓ | ✓ |
| single_file.py | ✓ | ✓ |
| single_file_utils.py | ✓ | ✓ |
| single_file_model.py | ✓ | ✓ |
| textual_inversion.py | ✓ | ✓ |
| utils.py | ✓ | ✓ |
| ip_adapter.py | ✓ | ✓ |
| t2i_adapter.py | ✓ | ✓ |
| peft_adapter_mixin.py | ✓ | ✓ |
| unet_loader.py | ✓ | ✓ |
| vae_loader.py | ✓ | ✓ |

## `hooks/` Directory

| File | HF | MindOne | Notes |
|------|----|--------|-------|
| *all standard hooks* | ✓ | ✓ | |
| **context_parallel.py** | ✗ | ✓ | NEW: Context parallelism |

## `guiders/` Directory

Identical structure in both libraries.

## `utils/` Directory

| File | HF | MindOne | Notes |
|------|----|--------|-------|
| constants.py | ✓ | ✓ | |
| deprecation_utils.py | ✓ | ✓ | |
| doc_utils.py | ✓ | ✓ | |
| dynamic_modules_utils.py | ✓ | ✓ | |
| hub_utils.py | ✓ | ✓ | |
| import_utils.py | ✓ | ✓ | |
| logging.py | ✓ | ✓ | |
| outputs.py | ✓ | ✓ | |
| pil_utils.py | ✓ | ✓ | |
| state_dict_utils.py | ✓ | ✓ | |
| torch_utils.py | ✓ | ✗ | Replaced by mindspore_utils.py |
| accelerate_utils.py | ✓ | ✗ | Not needed in MindSpore |
| dummy_*.py (12 files) | 12 | 0 | Optional dependency stubs |
| **mindspore_utils.py** | ✗ | ✓ | NEW: MindSpore-specific utils |

## `modular_pipelines/` Directory

| Subdirectory | HF | MindOne | Notes |
|--------------|----|--------|-------|
| flux/ | ✓ | ✓ | MindOne includes Flux2 |
| stable_diffusion_xl/ | ✓ | ✓ | Same |
| wan/ | ✓ | ✓ | Same |
| qwenimage/ | ✗ | ✓ | NEW in MindOne |

## Summary of Files Count

### HF Diffusers (src/diffusers/)

- models/: ~90 files (autoencoders + transformers + unets + controlnets + shared)
- pipelines/: ~95 pipeline directories
- schedulers/: 45 files
- loaders/: 12 files
- utils/: ~25 files

### MindOne Diffusers (mindone/diffusers/)

- models/: ~88 files (autoencoders + transformers + unets + controlnets + shared)
- pipelines.: ~90 pipeline directories
- schedulers.: 43 files
- loaders.: 12 files
- utils.: ~13 files

## Key Differences Summary

1. **Flax Support Removed**: All Flax-related files removed in MindOne
2. **ONNX Support Removed**: ONNX runtime pipelines not in MindOne
3. **MindSpore Utilities Added**: `mindspore_utils.py` replaces `torch_utils.py`
4. **Context Parallel Added**: `context_parallel.py` hook for distributed training
5. **New Models Added**: Flux2, Bria, Kandinsky5, QwenImage
6. **QwenImage Modular Pipeline**: New modular pipeline architecture
7. **Simplified Utils**: Fewer dummy dependency files, streamlined utilities