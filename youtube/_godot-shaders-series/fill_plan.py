#!/usr/bin/env python3
"""fill_plan.py: refreshes the generated parts of SERIES-PLAN.md (the table between TABLE markers) from SERIES-TABLE.md.
Run after series_table.py:  python3 series_table.py && python3 fill_plan.py"""
import re
from pathlib import Path
S = Path(__file__).resolve().parent
t = (S / "SERIES-TABLE.md").read_text()
m = re.search(r"(\| Film \|.*?)\n\n(\*\*Totals\.\*\*[^\n]*)", t, re.S)
table = m.group(1) + "\n\n" + m.group(2)
plan = (S / "SERIES-PLAN.md").read_text()
block = "<!-- TABLE:START -->\n## The twenty films in numbers\n\nRead from the films' own files (`series_table.py`). Minutes are the lint's ceiling estimate (every spoken word at 0.34 s, plus 4 s); the real length is known only after the voice is generated and usually comes out a little shorter.\n\n" + table + "\n<!-- TABLE:END -->"
plan = re.sub(r"<!-- TABLE:START -->.*?<!-- TABLE:END -->", lambda _: block, plan, flags=re.S)
(S / "SERIES-PLAN.md").write_text(plan)
print("table refreshed")
