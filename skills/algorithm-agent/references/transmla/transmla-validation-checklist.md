# TransMLA Validation Checklist

Use this checklist for a TransMLA-style bounded proving case or follow-on.

## Minimum validation

1. The config surface accepts the bounded feature settings and rejects invalid
   combinations when validation logic exists.
2. Baseline-off behavior preserves the original path.
3. The bounded feature-on path completes one focused forward smoke with the
   expected output shape.
4. Any claimed checkpoint-remap or load path works for the exact supported
   artifact shape.
5. Validation results are recorded with explicit status values such as `pass`,
   `fail`, `blocked`, `partial`, or `not_run`; unexecuted checks must not be
   implied as `pass`.

## Strongly recommended validation

1. Run a focused parity or semantic check for the exact bounded slice being
   claimed.
2. Run one cache/generation smoke if the bounded step explicitly includes a
   cache/runtime path.
3. Run the dtypes and backends that matter for the current bounded claim.
4. Run one remote or target-environment validation when local environment gaps
   would otherwise hide the real blocker.
5. Distinguish environment blockers from code sync issues and from real runtime
   contract failures.

## Example test ideas

### Baseline-off smoke

```python
config.transmla_variant = "none"
model = Model(config)
outputs = model(**inputs)
assert outputs[0].shape == (batch, seq, vocab)
```

### Bounded semantic-slice smoke

```python
config.transmla_variant = "split_rope_stubbed"
model = Model(config)
outputs = model(**inputs, use_cache=False)
assert outputs[0].shape == (batch, seq, vocab)
```

### Cache-path smoke

```python
config.transmla_variant = "split_rope_stubbed"
model = Model(config)
outputs = model(**inputs, use_cache=True)
cache = outputs[1]
assert cache is not None
_ = cache[0]
```

## Symptom-to-cause hints

- forward smoke fails before model code runs: likely environment or import
  blocker
- focused tests select nothing on the target machine: likely code-sync problem
- first cached run fails at indexed cache access: likely cache-construction or
  cache-layout contract mismatch
- semantic slice passes with `use_cache=False` but not with `use_cache=True`:
  runtime/cache should be treated as a separate follow-on
- evidence exists only for one narrow smoke: success wording must stay bounded

## Explicit non-claim discipline

A passing bounded TransMLA check does **not** imply:

- full TransMLA completion
- fuller MLA semantics
- paged runtime support
- broader MindSpore-native runtime completion
- training/serving readiness
- performance characterization
