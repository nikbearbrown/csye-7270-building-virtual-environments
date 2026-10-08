"""Summarize sweep.csv: per (mode, count) the min, median and max of the five
per-run mean frame times, the median p95, and the worst frame seen."""
import csv, statistics as st, sys
from collections import defaultdict
rows = list(csv.DictReader(open(sys.argv[1])))
g = defaultdict(list)
for r in rows:
    g[(r["mode"], int(r["count"]))].append(r)
print("count,mode,runs,min_mean_ms,median_mean_ms,max_mean_ms,median_p95_ms,worst_frame_ms,object_count,node_count,static_memory_mb")
for k in sorted(g, key=lambda k: (k[1], k[0] != "nodes")):
    m = [float(r["mean_ms"]) for r in g[k]]
    p = [float(r["p95_ms"]) for r in g[k]]
    x = [float(r["max_ms"]) for r in g[k]]
    r0 = g[k][0]
    print(f"{k[1]},{k[0]},{len(m)},{min(m):.3f},{st.median(m):.3f},{max(m):.3f},{st.median(p):.3f},{max(x):.1f},{r0['object_count']},{r0['node_count']},{r0['static_memory_mb']}")
