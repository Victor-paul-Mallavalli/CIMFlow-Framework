# analyze_logs.py
import os
import re

LOG_DIR = "logs"
SUMMARY_PATH = os.path.join(LOG_DIR, "cluster_summary.log")

total_cycles = []
vec_usage = 0
cim_usage = 0
scalar_usage = 0

print("[Cluster Log Analyzer]")

for filename in sorted(os.listdir(LOG_DIR)):
    if filename.startswith("core_") and filename.endswith(".log"):
        path = os.path.join(LOG_DIR, filename)
        print(f"  ➤ Reading {filename}")
        with open(path) as f:
            content = f.read()

        # Parse metrics
        cycles_match = re.search(r"Total Cycles: (\d+)", content)
        vec_match = re.search(r"VEC Usage: (\d+)", content)
        cim_match = re.search(r"CIM Usage: (\d+)", content)
        scalar_match = re.search(r"SCALAR Usage: (\d+)", content)

        if cycles_match:
            total_cycles.append(int(cycles_match.group(1)))
        if vec_match:
            vec_usage += int(vec_match.group(1))
        if cim_match:
            cim_usage += int(cim_match.group(1))
        if scalar_match:
            scalar_usage += int(scalar_match.group(1))

# Summary
summary = f"""
=== Cluster Performance Summary ===
Cores Simulated     : {len(total_cycles)}
Max Core Latency    : {max(total_cycles) if total_cycles else 0} cycles
Total VEC Usage     : {vec_usage}
Total CIM Usage     : {cim_usage}
Total SCALAR Usage  : {scalar_usage}
==============================
"""

# Write it
with open(SUMMARY_PATH, "w") as f:
    f.write(summary.strip())

print("✅ Cluster Summary written to logs/cluster_summary.log")
print(summary)
