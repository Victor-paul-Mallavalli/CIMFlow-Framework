import os

class OperatorOptimizer:
    def __init__(self, ir_dir="outputs/ir_dump", output_dir="outputs/ir_tiled", tile_size=16):
        self.ir_dir = ir_dir
        self.output_dir = output_dir
        self.tile_size = tile_size
        os.makedirs(self.output_dir, exist_ok=True)

    def tile_loop(self, op_line):
        """
        Simulate loop tiling on an operation.
        Example:
            Conv resnetv22_conv0_fwd ->
                TILE_LOOP 0: Conv resnetv22_conv0_fwd
                TILE_LOOP 1: Conv resnetv22_conv0_fwd
                ...
        """
        if not op_line.strip():
            return []

        try:
            op_type, op_name = op_line.strip().split(" ", 1)
        except ValueError:
            return [f"TILE_LOOP 0: UNKNOWN {op_line.strip()}"]

        return [f"TILE_LOOP {i}: {op_type} {op_name}" for i in range(self.tile_size)]

    def process_partition_ir(self, ir_path):
        with open(ir_path, "r") as f:
            lines = f.read().strip().split("\n")

        tiled_ir = []
        for line in lines:
            tiled_ir.extend(self.tile_loop(line))

        return tiled_ir

    def optimize(self):
        files = [f for f in os.listdir(self.ir_dir) if f.endswith(".ir")]
        if not files:
            print(f"[⚠️] No .ir files found in {self.ir_dir}")
            return

        for file in files:
            in_path = os.path.join(self.ir_dir, file)
            tiled_ir = self.process_partition_ir(in_path)

            out_file = file.replace(".ir", ".tiled.ir")
            out_path = os.path.join(self.output_dir, out_file)
            with open(out_path, "w") as f:
                f.write("\n".join(tiled_ir))

            print(f"[✅ OP-TILER] {file} → {out_file}")

if __name__ == "__main__":
    tiler = OperatorOptimizer()
    tiler.optimize()
