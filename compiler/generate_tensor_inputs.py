import os
import json
from collections import defaultdict

ISA_DIR = "outputs/isa_bin"
OUT_DIR = "outputs/tensor_inputs"
os.makedirs(OUT_DIR, exist_ok=True)

def extract_tensor_names(isa_dir):
    tensor_map = defaultdict(set)
    for file in os.listdir(isa_dir):
        if file.endswith(".isa"):
            pid = file.replace(".isa", "").split("_")[-1] 
            with open(os.path.join(isa_dir, file), "r") as f:
                for line in f:
                    if "//" in line:
                        comment = line.split("//")[1].strip()
                        if comment:
                            tensor_map[pid].add(comment)
    return tensor_map

def generate_tensor_inputs(tensor_map):
    for pid, tensors in tensor_map.items():
        input_data = {name: [1, 2, 3, 4] for name in tensors}  
        path = os.path.join(OUT_DIR, f"tensor_input_{pid}.json")
        with open(path, "w") as f:
            json.dump(input_data, f, indent=4)
        print(f"✅ Generated: {path}")

tensor_map = extract_tensor_names(ISA_DIR)
generate_tensor_inputs(tensor_map)
