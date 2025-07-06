import os

# List of directories to clean
directories = [
    "outputs/ir_dump",
    "outputs/ir_tiled",
    "outputs/isa_bin",
    "outputs/tensor_inputs",
    "logs"
]

def delete_files_only(folder):
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f" Deleted file: {item_path}")
        else:
            print(f"[KEEP] Skipping directory: {item_path}")

if __name__ == "__main__":
    print(" Cleaning generated files (not folders)...\n")
    for dir_path in directories:
        delete_files_only(dir_path)

    print("\n Cleanup complete.")
