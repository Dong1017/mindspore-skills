# Readiness Agent Contract

`readiness-agent` is the canonical public readiness entrypoint.

## Public Modes

```text
readiness-agent --mode check   # default
readiness-agent --mode fix
```

### `check`

`check` is the unified guided read-only assessment.

Responsibilities:

- Discover workspace evidence (target, launcher, framework, Python env, CANN, assets).
- Ask structured confirmation questions when inference is ambiguous.
- Run safe near-launch probes.
- Optionally run `task_smoke_cmd` **only after user confirmation**.
- Produce a readiness verdict: `READY`, `WARN`, or `BLOCKED`.
- Write the canonical readiness lock.
- Emit `portable_question` for host-native structured questions.
- Support `--confirm field=value` replay.
- Do not install packages, download assets, create virtual environments, edit
  source files or configs, scaffold files, or write `.readiness.env`.

Allowed statuses:

```text
NEEDS_CONFIRMATION
READY
WARN
BLOCKED
```

`NEEDS_CONFIRMATION` is a transient phase-gate. The final status after resolution
is always `READY`, `WARN`, or `BLOCKED`.

### `fix`

`fix` preserves the existing safe user-space remediation semantics.

Responsibilities:

- Run only when the user explicitly asks for remediation.
- Keep the legacy readiness fix dispatch path.
- May create or reuse workspace-local environments.
- May install user-space packages.
- May download explicitly declared assets when allowed by the existing fix policy.
- May write `.readiness.env`.
- Do not return `NEEDS_CONFIRMATION`.
- Reads the latest readiness lock before acting when available.
- Refreshes the lock after successful remediation.

Allowed statuses:

```text
READY
WARN
BLOCKED
```

## Assessment Scope

`readiness-agent --mode check` provides read-only launch-readiness
assessment for local single-machine NPU workspaces.

It verifies:

- target selection
- launcher selection
- selected Python and environment
- framework path
- CANN / Ascend runtime evidence
- asset source clarity
- near-launch probes

It does not verify:

- real training success
- real inference success
- accuracy correctness
- performance quality
- post-run failure causes

Those belong to downstream runtime, accuracy, performance, or failure workflows.

## Assessment Read-Only Rules

`check` may write readiness artifacts, but must not:

- install packages
- download model or dataset assets
- create virtual environments
- edit source files or configs
- scaffold files
- write `.readiness.env`
- run `task_smoke_cmd` without explicit user confirmation

If `task_smoke_cmd` is provided but not confirmed, `check` returns
`NEEDS_CONFIRMATION` for task smoke approval.

## Structured Confirmation Boundary

Python core emits `portable_question` and confirmation state only.

Host adapters must map `portable_question` to `AskUserQuestion` or an equivalent
UI, collect the response, and replay it as `--confirm field=value` before giving
a final answer. If the result is still `NEEDS_CONFIRMATION`, repeat the mapping
for the next field.

Python core must not call `AskUserQuestion`, block on `input()`, or depend on a
host-specific prompt API.

## Assessment Artifact Identity

Assessment artifacts must include:

```json
{
  "schema_version": "readiness.assessment.v1",
  "producer": "readiness-agent",
  "mode": "check",
  "engine": "assessment"
}
```

## Artifact Contract

The canonical downstream assessment artifact path is:

```text
readiness-output/latest/readiness-agent/*
```

This path is the stable machine-readable integration surface for downstream
agents.

Legacy compatibility artifacts are also written:

```text
readiness-output/report.json
readiness-output/report.md
readiness-output/meta/readiness-verdict.json
```

Run-scoped attempt artifacts may also be written under:

```text
readiness-output/attempts/<attempt_id>/current|final/*
```

Attempt artifacts are audit/debug trail only. Downstream integrations must not
depend on their raw verdict internals.
