import networkx as nx
import os
import json

class OperatorGrouper:
    def __init__(self, graph, output_dir="outputs"):
        self.graph = graph
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def fuse_patterns(self):
        grouped = nx.DiGraph()
        visited = set()
        group_id = 0

        for node in nx.topological_sort(self.graph):
            if node in visited:
                continue

            op_type = self.graph.nodes[node].get("op_type", "")
            group = [node]
            visited.add(node)

            successors = list(self.graph.successors(node))
            if op_type == "Conv" and successors:
                bn = successors[0]
                if self.graph.nodes[bn]["op_type"] == "BatchNormalization":
                    group.append(bn)
                    visited.add(bn)
                    successors2 = list(self.graph.successors(bn))
                    if successors2:
                        relu = successors2[0]
                        if self.graph.nodes[relu]["op_type"] == "Relu":
                            group.append(relu)
                            visited.add(relu)

            group_name = f"group_{group_id}"
            group_id += 1
            grouped.add_node(group_name, members=group)

            # Add edges between groups based on first node connections
            for pred in self.graph.predecessors(group[0]):
                pred_group = self._find_group(grouped, pred)
                if pred_group:
                    grouped.add_edge(pred_group, group_name)

        return grouped

    def _find_group(self, grouped_graph, node):
        for g in grouped_graph.nodes:
            if node in grouped_graph.nodes[g]["members"]:
                return g
        return None

    def save_grouped_graph(self, grouped_graph):
        # Save DOT file
        dot_path = os.path.join(self.output_dir, "grouped_cg.dot")
        nx.drawing.nx_pydot.write_dot(grouped_graph, dot_path)

        # Save JSON file
        json_path = os.path.join(self.output_dir, "grouped_cg.json")
        data = nx.node_link_data(grouped_graph)
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Grouped graph saved to:\n  - {dot_path}\n  - {json_path}")


if __name__ == "__main__":
    from compiler.graph_builder import ComputationGraph

    cg = ComputationGraph("models/resnet18.onnx")
    graph = cg.build_graph()

    grouper = OperatorGrouper(graph)
    grouped = grouper.fuse_patterns()
    grouper.save_grouped_graph(grouped)
