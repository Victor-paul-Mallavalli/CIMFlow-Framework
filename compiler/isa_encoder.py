import os

class ISAEncoder:
    def __init__(self, graph, ir_dir="outputs/ir_tiled", output_dir="outputs/isa_bin"):
        self.graph = graph
        self.ir_dir = ir_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def encode_instruction(self, tiled_line):
        """
        Encodes a single instruction with real operand names from graph.
        """
        try:
            prefix, rest = tiled_line.split(": ", 1)
            op_type, node_name = rest.split(" ", 1)
        except ValueError:
            return f"NOP R1, R2, R3  // UNKNOWN"

        opcode_map = {
            "Conv": "CIM_MVM",
            "Gemm": "CIM_MVM",
            "Relu": "VEC_RELU",
            "Add": "VEC_ADD",
        }

        opcode = opcode_map.get(op_type, "NOP")

        inputs = self.graph.nodes[node_name].get("inputs", [])
        output = self.graph.nodes[node_name].get("outputs", ["R3"])[0]

        while len(inputs) < 2:
            inputs.append(inputs[0] if inputs else "R1")

        rs, rt = inputs[0], inputs[1]

        return f"{opcode} {rs}, {rt}, {output}  // {node_name}"

    def encode_all(self):
        for file in os.listdir(self.ir_dir):
            if file.endswith(".tiled.ir"):
                path = os.path.join(self.ir_dir, file)
                with open(path, "r") as f:
                    lines = f.read().strip().split("\n")

                encoded = [self.encode_instruction(line) for line in lines]

                out_path = os.path.join(self.output_dir, file.replace(".tiled.ir", ".isa"))
                with open(out_path, "w") as f:
                    f.write("\n".join(encoded))
                print(f"[ISA] Encoded: {out_path}")


if __name__ == "__main__":
    from compiler.graph_builder import ComputationGraph
    from utils.config import load_arch_config
    
    cfg = load_arch_config("config/arch_config.json")
    cg = ComputationGraph("models/resnet18.onnx")
    graph = cg.build_graph()

    encoder = ISAEncoder(graph)
    encoder.encode_all()
