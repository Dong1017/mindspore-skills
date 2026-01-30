# Migration Analysis: Pipelines and Models

This document analyzes the current support status in mindone.diffusers and identifies pipelines/models that need migration.

## Current Status Summary

Based on the official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md):

- **Total Supported Pipelines**: ~205 (out of ~240+ total)
- **Fully Supported (inference: ✅)**: ~170+
- **Partial Support (fp32/fp16 verified, inference: ✖️)**: ~30+
- **Not Verified Yet (all ✖️)**: ~15

## Migration Priority Matrix

### HIGH PRIORITY - Popular Models with Inference Verification Gap

These models are widely used but have inference verification pending:

| Pipeline | Status | Priority | Notes |
|----------|--------|----------|-------|
| `chroma`, `chroma_img2img` | ✖️ inference | HIGH | New SoTA image model |
| `cogview4`, `cogview4_control` | ✖️ inference | HIGH | Text-to-image |
| `mochi` | ✖️ inference | HIGH | Video diffusion model |
| `lucy_edit` | ✖️ inference | HIGH | Image editing |
| `easyanimate` (all variants) | ✖️ | HIGH | Video generation |
| `cosmos` (all variants) | ✖️ | HIGH | Video generation |
| `stable_video_diffusion` | ✖️ | HIGH | Video generation (SVD) |
| `hunyuan_skyreels_image2video` | ✖️ | HIGH | Video generation |
| `i2vgen_xl` | ✖️ inference | HIGH | Image-to-video |
| `cosmisid` | ✖️ | HIGH | Consistency model |
| `hidream_image` | ✖️ inference | HIGH | Text-to-image |

### MEDIUM PRIORITY - Extended Model Variants

These are supported models but need img2img/inpaint/contain/control extensions:

| Pipeline Group | Base Supported | Missing Variants | Priority |
|----------------|----------------|------------------|----------|
| **Flux** | `flux` ✅ | flux_control, flux_fill, flux_img2img, flux_inpaint | MEDIUM |
| **QwenImage** | N/A | Full pipeline (qwenimage, qwenimage_edit, etc.) | MEDIUM |
| **Kandinsky2.2** | ✅ | kandinsky2_2_inpaint | MEDIUM |
| **CogVideoX** | ✅ | Various control variants fully verified | MEDIUM |

### LOW PRIORITY - Niche/Runtime Issues

Models with OOM issues or limited use cases:

| Pipeline | Status | Notes |
|----------|--------|-------|
| `kandinsky_prior` | ✖️ inference | Prior model not verified |
| `wuerstchen_prior` | ✖️ inference | Prior model not verified |
| `stable_cascade_prior` | ✖️ inference | Prior model not verified |

## Key Missing Models from HF Diffusers

Based on the HF diffusers source tree, the following models exist in HF but may need priority verification:

### New/Recent Models (Not in mindone or preview support)

1. **ChronosEdit** (editing pipeline) - Not found in mindone
2. **Additional ControlNet variants** - Some newer ControlNet models
3. **Adapter variants** - T2I-Adapter, IP-Adapter combinations

### Model-Specific Migration Needs

#### 1. Flux Family
```
Existing: flux ✅ (fp32/fp16 verified)
Missing/Need Verification:
├── flux_control (✖️)
├── flux_fill (✖️)
├── flux_img2img (✖️)
├── flux_inpaint (✖️)
├── flux_kontext (✖️)
├── flux_kontext_inpaint (✖️)
└── flux_prior_redux (✖️)
```

#### 2. Cosmos Family
```
Status: All ✖️
├── cosmos_text2world (✖️)
├── cosmos_video2world (✖️)
├── cosmos2_text2image (✖️)
└── cosmos2_video2world (✖️)
```

#### 3. EasyAnimate Family
```
Status: All ✖️
├── easyanimate (✖️)
├── easyanimate_control (✖️)
└── easyanimate_inpaint (✖️)
```

#### 4. CogView4 Family
```
Status: All ✖️
├── cogview4 (✖️)
└── cogview4_control (✖️)
```

#### 5. QwenImage (MindOne specific - need HF equivalent comparison)
```
Status: Model exists in mindone, HF verification needed
├── qwenimage (✖️ inference)
├── qwenimage_edit (✖️)
├── qwenimage_edit_inpaint (✖️)
├── qwenimage_img2img (✖️)
└── qwenimage_inpaint (✖️)
```

## Component Analysis

### Models Status

| Component Type | Total | Supported | Notes |
|----------------|-------|-----------|-------|
| AutoEncoders | 20 | 20 | All supported |
| ControlNets | 11 | 11 | All supported |
| Transformers | 38 | 38 | Includes Flux2, BRIA, Kandinsky5 |
| UNets | 16 | 16 | All standard UNets supported |

### Schedulers Status

| Component | Status |
|-----------|--------|
| Schedulers | 43 files, most standard schedulers supported |

## Migration Strategy

### Phase 1: High Priority SoTA Models

1. **Mochi** - Video generation (high community interest)
2. **LucyEdit** - Image editing
3. **Flux variants** (img2img, inpaint, control)
4. **EasyAnimate** - Video generation
5. **Cosmos family** - Video/text-to-video

### Phase 2: Popular Variants

1. Flux control/fill/kontext extensions
2. CogVideoX full control variants
3. Stable Video Diffusion (SVD)

### Phase 3: Niche/Experimental

1. Consistency model variants
2. Prior model workflows (Kandinsky, Wuerstchen, Cascade)

## Migration Workflow by Model Type

### Transformers (DiT-based)

For new transformer models like Flux2, Mochi, etc.:

1. Identify attention mechanism (scaled_dot_product vs custom)
2. Check for rotary embeddings
3. Verify group/query attention (GQA) support
4. Map attention mask handling

### Video Models

For video models (CogVideoX, SVD, EasyAnimate, Mochi):

1. Analyze temporal attention blocks
2. Check frame conditioning mechanisms
3. Consider temporal upsampling
4. Verify frame interpolation

### Control/Editing Models

For ControlNet, editing variants:

1. Verify control signal injection points
2. Check feature map compatibility
3. Test with existing base models

## Quick Reference: Add New Model

To add a new model:

1. **Check HF implementation** - `diffusers/src/diffusers/pipelines/[model_name]/`
2. **Check existing mindone model** - Similar models in `mindone/diffusers/models/`
3. **Follow migration workflow** - See [06-pipeline-migration.md](06-pipeline-migration.md)
4. **Update SUPPORT_LIST.md** - Add row for new model

## See Also

- [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) - Official support list
- [06-pipeline-migration.md](06-pipeline-migration.md) - Step-by-step migration workflow
- [05-mindone-specific.md](05-mindone-specific.md) - MindOne-specific components