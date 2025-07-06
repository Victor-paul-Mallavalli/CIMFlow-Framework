import os
import re
import json

LOG_DIR = "logs"
SUMMARY_FILE = os.path.join(LOG_DIR, "core_summary.txt")
SUMMARY_JSON = os.path.join(LOG_DIR, "core_summary.json")

# Energy per op in picojoules
ENERGY_COST = {
    "CIM": 3.5,
    "VEC": 1.2,
    "SCALAR": 0.8
}

def parse_perf_file(file_path):
    data = {
        "core": os.path.basename(file_path).replace("_perf.txt", ""),
        "cycles": 0,
        "CIM": 0,
        "VEC": 0,
        "SCALAR": 0,
    }
    with open(file_path, "r") as f:
        for line in f:
            if "Total Cycles" in line:
                data["cycles"] = int(re.findall(r"\d+", line)[0])
            elif "CIM Usage" in line:
                data["CIM"] = int(re.findall(r"\d+", line)[0])
            elif "VEC Usage" in line:
                data["VEC"] = int(re.findall(r"\d+", line)[0])
            elif "SCALAR Usage" in line:
                data["SCALAR"] = int(re.findall(r"\d+", line)[0])
    return data

def compute_energy(entry):
    return (
        entry["CIM"] * ENERGY_COST["CIM"] +
        entry["VEC"] * ENERGY_COST["VEC"] +
        entry["SCALAR"] * ENERGY_COST["SCALAR"]
    )

def main():
    summary = []
    totals = {"cycles": 0, "CIM": 0, "VEC": 0, "SCALAR": 0}
    max_cycles = 0
    for fname in sorted(os.listdir(LOG_DIR)):
        if fname.startswith("core_") and fname.endswith("_perf.txt"):
            path = os.path.join(LOG_DIR, fname)
            entry = parse_perf_file(path)
            entry["energy_pJ"] = compute_energy(entry)
            entry["latency_cycles"] = entry["cycles"]  # explicitly add latency
            summary.append(entry)

            for k in totals:
                totals[k] += entry[k]
            max_cycles = max(max_cycles, entry["cycles"])
            print(max_cycles)
    total_energy = compute_energy(totals)
    ops_total = totals["CIM"] + totals["VEC"] + totals["SCALAR"]

    with open(SUMMARY_FILE, "w") as out:
        out.write("=== Multi-Core Simulation Summary ===\n")
        for entry in summary:
            out.write(f"\n[ {entry['core']}]\n")
            out.write(f"  Latency (Cycles): {entry['latency_cycles']}\n")
            out.write(f"  CIM Ops         : {entry['CIM']}\n")
            out.write(f"  VEC Ops         : {entry['VEC']}\n")
            out.write(f"  SCALAR Ops      : {entry['SCALAR']}\n")
            out.write(f"  Estimated Energy: {entry['energy_pJ']:.2f} pJ\n")

        out.write("\n[ Aggregated Stats]\n")
        out.write(f"  Total Cycles    : {max_cycles}\n")
        out.write(f"  Total CIM Ops   : {totals['CIM']}\n")
        out.write(f"  Total VEC Ops   : {totals['VEC']}\n")
        out.write(f"  Total SCALAR Ops: {totals['SCALAR']}\n")
        out.write(f"  Total Ops       : {ops_total}\n")
        out.write(f"  Total Energy    : {total_energy:.2f} pJ\n")
        if totals["cycles"]:
            out.write(f"  Ops per Cycle   : {ops_total / totals['cycles']:.2f}\n")
            
    totals["cycles"] = max_cycles
    with open(SUMMARY_JSON, "w") as jf:
        json.dump({"summary": summary, "totals": totals, "total_energy_pJ": total_energy}, jf, indent=2)

    print(f"\n Summary written to: {SUMMARY_FILE}")
    print(f" JSON written to: {SUMMARY_JSON}")

if __name__ == "__main__":
    main()
