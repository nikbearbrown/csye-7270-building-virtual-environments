"""Trim a Claude Code stream-json or Codex --json transcript for the course repo.
Drops system/hook events (local environment listings); keeps assistant text, tool calls,
tool results, and the final result; replaces the scratch path with <scratch>."""
import json, sys
SCRATCH = "/path/to/your/scratch/work"  # prefix replaced with <scratch>
src, dst = sys.argv[1], sys.argv[2]
kept = 0
with open(src) as f, open(dst, "w") as out:
    for line in f:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = e.get("type")
        if t == "system":
            if e.get("subtype") == "init":
                e = {"type": "system", "subtype": "init", "model": e.get("model"),
                     "permissionMode": e.get("permissionMode"),
                     "claude_code_version": e.get("claude_code_version"),
                     "note": "tool, MCP, plugin and skill listings removed for the course record"}
            else:
                continue
        if t in ("rate_limit_event",):
            continue
        if t == "assistant":
            for c in e.get("message", {}).get("content", []):
                if isinstance(c, dict):
                    c.pop("signature", None)
        if t == "result":
            e = {k: e.get(k) for k in ("type", "subtype", "is_error", "num_turns", "duration_ms",
                                      "result", "permission_denials", "terminal_reason")}
        s = json.dumps(e, ensure_ascii=False).replace(SCRATCH, "<scratch>")
        s = s.replace("~/", "~/")
        out.write(s + "\n")
        kept += 1
print(dst, kept, "events kept")
