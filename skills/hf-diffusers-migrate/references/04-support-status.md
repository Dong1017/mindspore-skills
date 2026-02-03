# Migration Support Status

Based on official [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md).

## Current Status

- **Total Supported Pipelines**: ~205 (out of ~240+)
- **Fully Supported (inference: ✅)**: ~170+
- **Partial Support (fp32/fp16 verified, inference: ✖️)**: ~30+
- **Not Verified Yet (all ✖️)**: ~15

## HIGH PRIORITY - Models with Inference Verification Gap

| Pipeline | Status | Notes |
|----------|--------|-------|
| `chroma`, `chroma_img2img` | ✖️ inference | New SoTA image model |
| `cogview4`, `cogview4_control` | ✖️ inference | Text-to-image |
| `mochi` | ✖️ inference | Video diffusion model |
| `lucy_edit` | ✖️ inference | Image editing |
| `easyanimate` (all variants) | ✖️ | Video generation |
| `cosmos` (all variants) | ✖️ | Video generation |
| `stable_video_diffusion` | ✖️ | Video generation (SVD) |
| `hunyuan_skyreels_image2video` | ✖️ | Video generation |
| `i2vgen_xl` | ✖️ inference | Image-to-video |
| `cosmisid` | ✖️ | Consistency model |
| `hidream_image` | ✖️ inference | Text-to-image |

## MEDIUM PRIORITY - Extended Model Variants

| Pipeline Group | Base Supported | Missing Variants |
|----------------|----------------|------------------|
| **Flux** | `flux` ✅ | flux_control, flux_fill, flux_img2img, flux_inpaint |
| **QwenImage** | N/A | Full pipeline (qwenimage, qwenimage_edit, etc.) |
| **Kandinsky2.2** | ✅ | kandinsky2_2_inpaint |
| **CogVideoX** | ✅ | Various control variants |

## Component Status

| Component | Total | Supported |
|-----------|-------|-----------|
| AutoEncoders | 20 | 20 |
| ControlNets | 11 | 11 |
| Transformers | 38 | 38 (includes Flux2, Bria, Kandinsky5) |
| UNets | 16 | 16 |
| Schedulers | 43 | most standard schedulers supported |

## Quick Reference: Add New Model

To add a new model:

1. **Check HF implementation** - `diffusers/src/diffusers/pipelines/[model_name]/`
2. **Check existing mindone model** - Similar models in `mindone/diffusers/models/`
3. **Run auto_convert.py** - Use automated conversion first:
   ```bash
   python auto_convert.py --src_root /path/to/hf/diffusers --dst_root /path/to/mindone/diffusers
   ```
4. **Fix unmapped interfaces** - Review converter output log
5. **Update SUPPORT_LIST.md** - Add row for new model

## Links

- [SUPPORT_LIST.md](https://github.com/mindspore-lab/mindone/blob/master/mindone/diffusers/SUPPORT_LIST.md) - Official support list