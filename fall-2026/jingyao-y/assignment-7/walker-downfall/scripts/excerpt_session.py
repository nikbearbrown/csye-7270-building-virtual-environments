"""Labelled excerpt of an agent-session transcript (JSONL) for the A6 upload.

The full transcripts exceed the course's ~1 MB limit. The excerpt keeps, in
order: a header record, the first user message (the prompt and tool rules) in
full, every tool call (name + input cut to 400 chars; the final report handed back
to the main session is kept in full), every tool result cut to
400 chars (errors flagged), and the final assistant text in full. Nothing is
reworded; cut fields end with "…[cut N chars]".

    python scripts/excerpt_session.py sessions/session-2.jsonl
"""
import json, os, sys, hashlib

CUT = 400

def cut(s):
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    return s if len(s) <= CUT else s[:CUT] + f"…[cut {len(s) - CUT} chars]"

def main(path):
    raw = open(path, "rb").read()
    lines = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    out = [{"excerpt_of": os.path.basename(path), "full_bytes": len(raw), "full_sha256": hashlib.sha256(raw).hexdigest(),
            "full_records": len(lines), "rule": __doc__.strip().splitlines()[2:7]}]
    first_user = True
    last_text = None
    for d in lines:
        m = d.get("message") or {}
        c = m.get("content")
        if d.get("type") == "user" and first_user:
            out.append({"type": "prompt", "content": c})
            first_user = False
            continue
        if isinstance(c, list):
            for x in c:
                if x.get("type") == "tool_use":
                    full = "handback" in str(x.get("name", "")).lower()
                    out.append({"type": "tool_use", "name": x.get("name"), "input": x.get("input") if full else cut(x.get("input"))})
                elif x.get("type") == "tool_result":
                    out.append({"type": "tool_result", "is_error": bool(x.get("is_error")), "content": cut(x.get("content"))})
                elif x.get("type") == "text" and m.get("role") == "assistant":
                    last_text = x.get("text")
    out.append({"type": "final_assistant_text", "text": last_text})
    dst = path.replace(".jsonl", ".excerpt.jsonl")
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        for r in out: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(dst, os.path.getsize(dst))

for p in sys.argv[1:]: main(p)
