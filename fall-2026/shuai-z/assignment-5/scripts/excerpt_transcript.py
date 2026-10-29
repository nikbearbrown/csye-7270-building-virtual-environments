#!/usr/bin/env python3
"""Writes a labelled excerpt of a `claude -p --output-format stream-json`
transcript that is over the assignment's limit of about 1 MB.

    python3 -I scripts/excerpt_transcript.py FULL.jsonl EXCERPT.jsonl SOURCE

The excerpt keeps every event, in order. It cuts only two fields of
`tool_use_result`, the harness's structured copy of a tool's result. The
copy in `message.content`, the result the agent was given, stays whole.
- `originalFile`: the whole file as it was before an Edit or a Write.
- `stdout`: only where it is identical to the result in the same event's
  `message.content`.
Each cut value becomes a marker giving its size and SOURCE, the place where
the full transcript is kept. Every other line is copied byte for byte.
"""
import json
import sys


def result_text(event):
    """The tool result in the event's message.content, as one string, or None."""
    content = event.get("message", {}).get("content")
    if not isinstance(content, list):
        return None
    for part in content:
        if isinstance(part, dict) and part.get("type") == "tool_result":
            value = part.get("content")
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                return "\n".join(p.get("text", "") for p in value if isinstance(p, dict))
    return None


def marker(value, why, source):
    return f"[excerpt: {len(value.encode()):,} bytes cut, {why}. Full transcript: {source}]"


def main(full_path, excerpt_path, source):
    with open(full_path, "rb") as f:
        lines = f.read().split(b"\n")
    out = []
    cut = {"originalFile": [0, 0], "stdout": [0, 0]}
    for line in lines:
        if not line:
            out.append(line)
            continue
        event = json.loads(line)
        copy = event.get("tool_use_result")
        changed = False
        if isinstance(copy, dict):
            original = copy.get("originalFile")
            if isinstance(original, str):
                cut["originalFile"][0] += 1
                cut["originalFile"][1] += len(original.encode())
                copy["originalFile"] = marker(original, "the file as it was before this edit", source)
                changed = True
            stdout = copy.get("stdout")
            if isinstance(stdout, str) and stdout and stdout == result_text(event):
                cut["stdout"][0] += 1
                cut["stdout"][1] += len(stdout.encode())
                copy["stdout"] = marker(stdout, "identical to this event's message.content", source)
                changed = True
        if changed:
            line = json.dumps(event, ensure_ascii=False, separators=(",", ":")).encode()
        out.append(line)
    data = b"\n".join(out)
    with open(excerpt_path, "wb") as f:
        f.write(data)
    events = sum(1 for l in lines if l)
    print(f"{events} events; {len(b''.join(lines)) + len(lines) - 1:,} bytes in, {len(data):,} bytes out")
    for field, (count, size) in cut.items():
        print(f"cut {field}: {count} values, {size:,} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
