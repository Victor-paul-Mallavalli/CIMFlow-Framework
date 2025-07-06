import networkx as nx
from utils.config import load_arch_config
import re
import json

class CGOptimizer:
    def __init__(self, graph, config, use_stage_partition=True):
        self.graph = graph
        self.config = config
        self.memory_limit = config["hardware"]["core"]["local_mem"]
        self.use_stage_partition = use_stage_partition
        self.partitions = []
        self.partition_map = {}
        self.memory_map = {node: self.estimate_memory(node) for node in graph.nodes}

    def estimate_memory(self, node):
        return self.graph.nodes[node].get("size_bytes", 4 * 1024)

    def extract_stage(self, name):
        match = re.search(r"stage\d+", name)
        if match:
            return match.group(0)
        elif "conv0" in name or "batchnorm0" in name:
            return "stage0"
        elif "dense" in name or "flatten" in name:
            return "stage_out"
        else:
            return "misc"

    def group_by_stage(self):
        stage_dict = {}
        for node in self.graph.nodes:
            stage = self.extract_stage(node)
            if stage not in stage_dict:
                stage_dict[stage] = []
            stage_dict[stage].append(node)
        return list(stage_dict.values())

    def stage_partition(self):
        stage_groups = self.group_by_stage()
        for pid, group in enumerate(stage_groups):
            self.partitions.append(group)
            for node in group:
                self.partition_map[node] = pid

    # def greedy_partition(self):
    #     nodes = list(nx.topological_sort(self.graph))
    #     current_partition, current_memory, pid = [], 0, 0

    #     for node in nodes:
    #         mem = self.memory_map[node]
    #         if current_memory + mem > self.memory_limit:
    #             self._finalize_partition(current_partition, pid)
    #             pid += 1
    #             current_partition, current_memory = [node], mem
    #         else:
    #             current_partition.append(node)
    #             current_memory += mem

    #     if current_partition:
    #         self._finalize_partition(current_partition, pid)

    # def _finalize_partition(self, nodes, pid):
    #     self.partitions.append(nodes)
    #     for n in nodes:
    #         self.partition_map[n] = pid

    def dynamic_partition(self):
        if self.use_stage_partition:
            self.stage_partition()
        else:
            self.greedy_partition()
        return self.partitions, self.partition_map

    def print_partitions(self):
        print(f"\n[🔧 CGOptimizer] Memory limit per partition: {self.memory_limit // 1024} KB")
        for i, part in enumerate(self.partitions):
            mvm_count = sum(1 for node in part if self.graph.nodes[node].get("is_mvm"))
            print(f"🧩 Partition {i} | Ops: {len(part)} | MVM Ops: {mvm_count}")
            print(f"   └─ {part}")

    def save_partition_map(self, path="partition_map.json"):
        with open(path, "w") as f:
            json.dump(self.partition_map, f, indent=2)
        print(f"[💾] Partition map saved to {path}")

if __name__ == "__main__":
    from compiler.graph_builder import ComputationGraph

    cfg = load_arch_config("config/arch_config.json")
    cg = ComputationGraph("models/resnet18.onnx")
    graph = cg.build_graph()
    optimizer = CGOptimizer(graph, cfg, use_stage_partition=True)
    partitions, mapping = optimizer.dynamic_partition()
    optimizer.print_partitions()
    optimizer.save_partition_map("../outputs/partition_map.json")