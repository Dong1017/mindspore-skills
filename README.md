# MindSpore Skills

MindSpore development skills for AI coding agents. Route operator work, migrate models, and diagnose readiness, failure, accuracy, and performance issues with guided workflows.

Compatible with **Claude Code**, **OpenCode**, **Gemini CLI**, and **Codex**.

## Installation

### Claude Code

Register the marketplace and install:

```
/plugin marketplace add mindspore-lab/mindspore-skills
/plugin install ms@mindspore-skills
```

Then use slash command:

```
/ms:diagnose
/ms:fix
/ms:migrate
```

### OpenCode

OpenCode loads custom commands from `commands/` and skills from `skills/`.

For a specific project, clone this repository into `.opencode`:

```bash
git clone https://github.com/mindspore-lab/mindspore-skills.git .opencode
```

This gives OpenCode the expected layout:

```text
.opencode/commands/
.opencode/skills/
```

For a global install, copy or symlink the contents into your existing OpenCode
directories instead of replacing the whole directory:

```bash
git clone https://github.com/mindspore-lab/mindspore-skills.git ~/.config/opencode/mindspore-skills
mkdir -p ~/.config/opencode/skills ~/.config/opencode/commands
ln -s ~/.config/opencode/mindspore-skills/skills/* ~/.config/opencode/skills/
ln -s ~/.config/opencode/mindspore-skills/commands/* ~/.config/opencode/commands/
```

Then in OpenCode:

```
/diagnose
/fix
/migrate
```

Specialist capabilities such as operator work, readiness checks, accuracy
analysis, and algorithm adaptation remain available as skills and routed
workflows rather than public slash commands.

See [OpenCode Skills docs](https://opencode.ai/docs/skills) and [OpenCode Commands docs](https://opencode.ai/docs/commands) for more details.

### Gemini CLI

Install as an extension:

```bash
gemini extensions install https://github.com/mindspore-lab/mindspore-skills.git --consent
```

Or from local clone:

```bash
git clone https://github.com/mindspore-lab/mindspore-skills.git
gemini extensions install ./mindspore-skills --consent
```

See [Gemini CLI extensions docs](https://geminicli.com/docs/extensions/) for more details.

### Codex

Codex does not install slash commands from this repository. It follows the
instructions it discovers from `AGENTS.md` files in the active project.

If you are working in this repository, no extra install step is needed. Open
the repo in Codex and it will read [AGENTS.md](/home/weizheng/work/mindspore-skills/AGENTS.md).

If you want to reuse this guidance in another project, copy or adapt the
relevant sections into that project's `AGENTS.md`. For shared personal defaults
across projects, you can also place guidance in `~/.codex/AGENTS.md`.

To verify instruction loading in this repository:

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

To verify instruction loading in another project:

```bash
codex --cd /path/to/your/project --ask-for-approval never "Show which instruction files are active."
```

See [Codex AGENTS guide](https://developers.openai.com/codex/guides/agents-md) for more details.

## Available Skills

### Operator Development

| Skill | Description |
|-------|-------------|
| `api-helper` | Find API call chains and operator wiring in MindSpore codebase |
| `operator-agent` | Route and build `torch` or `mindspore` operators through custom-access or native-framework integration, with MindSpore API-resolution and `op_info` verification support |

### Model Migration

| Skill | Description |
|-------|-------------|
| `migrate-agent` | Top-level model migration entry that analyzes the source repo, selects the correct migration route, and verifies the result |

### Diagnosis and Optimization

| Skill | Description |
|-------|-------------|
| `accuracy-agent` | Diagnose accuracy regressions, drift, wrong results, and cross-platform mismatch after successful execution |
| `algorithm-agent` | Adapt a paper feature or released reference implementation into an existing model codebase, including specialized routes such as mHC integration, and prepare the patch for readiness validation |
| `readiness-agent` | Check whether a local single-machine workspace is ready to train or run inference before execution |
| `failure-agent` | Diagnose MindSpore and PTA (torch_npu) training and runtime failures with evidence-backed root-cause validation |
| `performance-agent` | Diagnose throughput, latency, memory, utilization, dataloader, and communication bottlenecks after the workload already runs |

## Available Commands

| Command | Description |
|---------|-------------|
| `/diagnose` | Top-level symptom router for failure, accuracy, and performance diagnosis |
| `/fix` | Top-level symptom router for diagnose + propose + confirm + apply + verify |
| `/migrate` | Migration router (HF/third-party), routing only |

## Usage Examples

### Diagnose a training problem

```
/diagnose my qwen3 lora run crashes with operator not implemented on ascend
```

### Diagnose and fix a training problem

```
/fix throughput is only 340 tok/s on npu, expected 520
```

### Route a migration request

```
/migrate port this HuggingFace qwen2 repo to MindSpore
```

### Examples

See `examples/README.md` for the current example inventory and status.

Other capabilities can be triggered by describing the task directly, for
example operator implementation, readiness validation, or algorithm changes such
as mHC.

## Contract and Tests

- Architecture overview:
  - `docs/concepts/agent-architecture-overview.md`
- Contract docs:
  - `docs/concepts/skills-contract.md`
  - `docs/concepts/artifacts-and-reporting.md`
- Cross-skill contract tests: `tests/contract/`
- Skill-specific tests: `skills/<skill>/tests/`

## Repository Structure

```
mindspore-skills/
├── commands/                # Slash commands
│   ├── diagnose.md          # Symptom router for diagnose mode
│   ├── fix.md               # Symptom router for fix mode
│   ├── migrate.md           # Migration router
│   └── ...
├── skills/                  # Skill definitions
│   ├── api-helper/          # MindSpore API call-chain discovery
│   ├── migrate-agent/       # Top-level model migration entry
│   ├── operator-agent/      # Framework operator implementation
│   ├── readiness-agent/     # Single-machine workspace readiness and preflight
│   ├── accuracy-agent/      # Accuracy diagnosis after successful execution
│   ├── algorithm-agent/     # Feature adaptation and route-specific patch planning for existing models
│   ├── failure-agent/       # Training and runtime failure diagnosis
│   └── performance-agent/   # Performance diagnosis after the workload already runs
├── AGENTS.md                # Codex instructions
├── CLAUDE.md                # Claude-facing repository notes
└── gemini-extension.json    # Gemini CLI config
```

## Contributing

Contributions are welcome. Please submit a pull request.

When adding a new skill:
1. Add `skills/<skill-name>/SKILL.md` with matching frontmatter and directory name
2. Add a slash command in `commands/<command-name>.md` only if the skill should be part of the small public command surface
3. Update `AGENTS.md` (skill table + activation triggers)
4. Update `README.md` (skill list and commands)
5. Update `gemini-extension.json` with name/path/description
6. Update `CLAUDE.md` if Claude-facing setup or maintenance notes changed

When modifying an existing skill:
1. Update `skills/<skill-name>/SKILL.md` and any referenced files
2. Refresh `AGENTS.md` triggers if scope/keywords changed
3. Update `README.md` if descriptions or commands changed
4. Update `gemini-extension.json` if name/path/description changed

tools:
- Run `python tools/check_consistency.py` before submit
- (Optional) Install git hooks with `python tools/install_git_hooks.py`
- Tip: set up hooks with `make hooks` (see Makefile).

## License

Apache 2.0
