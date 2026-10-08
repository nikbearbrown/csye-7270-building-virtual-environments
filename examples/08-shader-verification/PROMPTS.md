# Prompts — Example 08

## Executive summary

These are the exact prompts and command lines used for Chapter 8's worked run on 2026-09-27, in a scratch copy of `walker-jumpman-clawd` at the Chapter 6 end state plus the seeded commit `2473fd8`:

- Claude Code 2.1.150 (`claude-sonnet-4-6`) reviewed the change.
- Codex CLI 0.153.4 (`gpt-5.6-sol`, reasoning effort `low`) reviewed it in a separate clone, then built the evidence and the fix, after the Claude account reached its session limit.

## Prompt 1 — review (both agents, identical)

The prompt text is `prompts/prompt-1-review.txt`, printed in full in Chapter 8.

Claude Code (read-only tools):

```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p "$(cat prompt-1-review.txt)" --allowedTools "Read,Glob,Grep,Bash(git:*),Bash(godot --headless:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose < /dev/null > session-1-review-claude.jsonl
```

Outcome: 18 turns, about 4.5 minutes; "DO NOT MERGE"; both bugs found.

Codex (separate clone of the same commit):

```bash
codex exec -s workspace-write --json -o session-1-review-codex-last.txt "$(cat prompt-1-review.txt)" < /dev/null > session-1-review-codex.jsonl
```

Outcome: 5 commands; "do not merge"; both bugs found. It edited no files.

## Prompt 2 — evidence before any fix

The prompt text is `prompts/prompt-2-evidence.txt`, printed in full in Chapter 8.

A Claude Code run of this prompt (same flags as Chapter 6's build session, `--max-turns 80`) stopped after nine read-only tool calls; see `README.md`, *Incident*. The run that produced the evidence was Codex:

```bash
codex exec -s workspace-write --json -o session-2-evidence-codex-last.txt "$(cat prompt-2-evidence.txt)" < /dev/null > session-2-evidence-codex.jsonl
```

Outcome: it created `verify_flash_spec.gd`, `flash_model.gd`, `flash_bench.gd`, `flash_bench.tscn`, `test_flash_bench.gd` and `BENCH.md`, and added a `FRICTIONAL.md` entry. Human review (commit `7149a4a`) corrected the oracle tolerance after testing it against the known-good code, and corrected the entry's attribution.

## Prompt 3 — the fix

The prompt text is `prompts/prompt-3-fix.txt`, printed in full in Chapter 8.

```bash
codex exec -s workspace-write --json -o session-3-fix-codex-last.txt "$(cat prompt-3-fix.txt)" < /dev/null > session-3-fix-codex.jsonl
```

Outcome: 8 commands. The shader went back to `COLOR`, and the flash back to `retry_remaining / 0.55`; all requested checks passed. Human review (commit `081c7c0`) corrected the attribution again and added a rounding note to `BENCH.md`.

## Our verification (not an agent prompt)

On the fixed commit, each with `timeout 120` and `--headless`:

- the three original suites at `--fixed-fps 60`;
- `test_flash.gd`, `verify_flash.gd` and `verify_flash_spec.gd` at 30, 60 and 144;
- `flash_model.gd` and `test_flash_bench.gd` at 60.

Every log was grepped for `SHADER ERROR`. Logs: `logs/fixed-*.log`.
