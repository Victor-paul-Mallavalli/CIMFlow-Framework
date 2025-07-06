# import os
# import json

# def load_outputs(log_dir):
#     outputs = {}
#     for fname in sorted(os.listdir(log_dir)):
#         if fname.startswith("core_") and fname.endswith("_output.json"):
#             path = os.path.join(log_dir, fname)
#             with open(path, "r") as f:
#                 outputs[fname] = json.load(f)
#     return outputs

# def is_empty_tensor(tensor):
#     return isinstance(tensor, list) and (len(tensor) == 0 or all(v == 0 for v in tensor))

# def validate_outputs(core_outputs, tolerance=0):
#     print("\n🧪 Running Output Validation...\n")
#     total_tensors = 0
#     empty_tensors = 0

#     for core_file, tensors in core_outputs.items():
#         print(f"🔍 Validating {core_file}")
#         for name, values in tensors.items():
#             total_tensors += 1
#             if is_empty_tensor(values):
#                 print(f"⚠️  Tensor '{name}' is empty or zero.")
#                 empty_tensors += 1

#     print("\n📊 Validation Summary:")
#     print(f"  Total output tensors: {total_tensors}")
#     print(f"  Empty tensors found : {empty_tensors}")
#     print("✅ Validation completed.\n")

# def main():
#     log_dir = "logs"  # adjust if needed
#     if not os.path.exists(log_dir):
#         print("❌ logs/ directory not found.")
#         return

#     core_outputs = load_outputs(log_dir)
#     validate_outputs(core_outputs)

# if __name__ == "__main__":
#     main()
