import onnx
import networkx as nx
import numpy as np
import json
from onnx import numpy_helper

class ComputationGraph:
    def __init__(self, onnx_path):
        self.onnx_path = onnx_path
        self.model = onnx.load(onnx_path)
        self.graph = self.model.graph
        self.cg = nx.DiGraph()

    def build_graph(self):
        name_map = {}

        for init in self.graph.initializer:
            size = self._estimate_size(init.dims)
            self.cg.add_node(
                init.name,
                op_type="Initializer",
                shape=list(init.dims),
                size_bytes=size,
                is_mvm=False
            )

        for node in self.graph.node:
            op_name = node.name or f"{node.op_type}_{id(node)}"
            tensor_bytes = 0
            for out in node.output:
                for vi in self.graph.value_info:
                    if vi.name == out:
                        shape = [d.dim_value for d in vi.type.tensor_type.shape.dim]
                        elem_size = 4 
                        tensor_bytes += np.prod(shape) * elem_size

            is_mvm = node.op_type in {"Conv", "Gemm"}

            self.cg.add_node(
                op_name,
                op_type=node.op_type,
                inputs=list(node.input),
                outputs=list(node.output),
                size_bytes=tensor_bytes,
                is_mvm=is_mvm
            )

            name_map.update({out: op_name for out in node.output})

        for node in self.graph.node:
            op_name = node.name or f"{node.op_type}_{id(node)}"
            for inp in node.input:
                if inp in name_map:
                    self.cg.add_edge(name_map[inp], op_name)

        return self.cg

    def _estimate_size(self, shape):
        if not shape:
            return 0
        return int(np.prod(shape)) * 4  

    def visualize_graph(self):
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.cg)
        nx.draw(self.cg, pos, with_labels=True, node_color='skyblue', edge_color='gray')
        labels = nx.get_node_attributes(self.cg, 'op_type')
        nx.draw_networkx_labels(self.cg, pos, labels)
        plt.show()

    def save_as_dot(self, path="cg.dot"):
        nx.drawing.nx_pydot.write_dot(self.cg, path)

    def save_as_json(self, path="cg.json"):
        data = nx.node_link_data(self.cg)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    cg = ComputationGraph("models/resnet18.onnx")
    graph = cg.build_graph()
    print(f"Constructed CG with {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
    cg.visualize_graph()
    cg.save_as_dot("cg.dot")
    cg.save_as_json("cg.json")
