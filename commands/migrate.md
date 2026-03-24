---
description: Route to MindSpore migration tools (HF models, third-party repos)
---

# MindSpore Migration Tools

Select a migration type:

| Type | Command | Description |
|------|---------|-------------|
| **Models and Repos** | `/model-agent` | Migrate Hugging Face models, diffusers pipelines, and generic PyTorch repos to MindSpore |

## Usage

```
/migrate hf       -> routes to /model-agent
/migrate model    -> routes to /model-agent
/migrate repo     -> routes to /model-agent
```

If no type specified, ask user what they want to migrate.
