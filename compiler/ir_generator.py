import os
from compiler.cg_optimizer import CGOptimizer

class IRGenerator:
    def __init__(self, graph, partition_map, output_dir="outputs/ir_dump"):
        self.graph = graph
        self.partition_map = partition_map
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_ir(self):
        """
        Generates a pseudo-IR per partition (core), listing op_type and node name.
        Output files are saved as partition_0.ir, partition_1.ir, ...
        """
        partition_ir = {}

        # Group ops by partition
        for node in self.graph.nodes:
            pid = self.partition_map.get(node, -1)
            if pid == -1:
                continue
            if pid not in partition_ir:
                partition_ir[pid] = []
            op_type = self.graph.nodes[node].get('op_type', 'UNKNOWN')
            partition_ir[pid].append(f"{op_type} {node}")

        # Write each partition to a separate file: partition_<id>.ir
        for pid, ops in partition_ir.items():
            file_path = os.path.join(self.output_dir, f"partition_{pid}.ir")
            with open(file_path, "w") as f:
                f.write("\n".join(ops))
            print(f"[IR] Written: {file_path}")

        return partition_ir

if __name__ == "__main__":
    from compiler.graph_builder import ComputationGraph
    from compiler.cg_optimizer import CGOptimizer
    from utils.config import load_arch_config

    cfg = load_arch_config("config/arch_config.json")
    cg = ComputationGraph("models/resnet18.onnx")
    graph = cg.build_graph()

    optimizer = CGOptimizer(graph, cfg, use_stage_partition=True)
    _, mapping = optimizer.dynamic_partition()

    irgen = IRGenerator(graph, mapping)
    irgen.generate_ir()
