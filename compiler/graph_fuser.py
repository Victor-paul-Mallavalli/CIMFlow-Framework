import networkx as nx
import copy

class GraphFuser:
    def __init__(self, graph):
        self.original_graph = graph
        self.graph = copy.deepcopy(graph)
        self.fused_graph = nx.DiGraph()
        self.fusion_patterns = [
            ("Conv", "Relu"),           # Conv -> ReLU
            ("BatchNormalization", "Relu", "Add"),  # BatchNorm → ReLU → Add
        ]
        self.fused_count = 0

    def fuse_patterns(self):
        for node in list(self.graph.nodes()):
            op_type = self.graph.nodes[node]["op_type"]

            # Conv → Relu
            if op_type == "Conv":
                children = list(self.graph.successors(node))
                if len(children) == 1 and self.graph.nodes[children[0]]["op_type"] == "Relu":
                    fused_name = f"FusedConvRelu_{self.fused_count}"
                    self._fuse_nodes([node, children[0]], fused_name, "ConvRelu")
                    self.fused_count += 1

            # BatchNorm → ReLU → Add
            if op_type == "BatchNormalization":
                bn_child = list(self.graph.successors(node))
                if len(bn_child) == 1 and self.graph.nodes[bn_child[0]]["op_type"] == "Relu":
                    relu_child = list(self.graph.successors(bn_child[0]))
                    if len(relu_child) == 1 and self.graph.nodes[relu_child[0]]["op_type"] == "Add":
                        fused_name = f"FusedBNReluAdd_{self.fused_count}"
                        self._fuse_nodes([node, bn_child[0], relu_child[0]], fused_name, "BNReluAdd")
                        self.fused_count += 1

        return self.graph

    def _fuse_nodes(self, nodes_to_fuse, new_node_name, op_type):
        # Add new fused node
        self.graph.add_node(new_node_name, op_type=op_type)

        # Connect predecessors of the first node to the fused node
        for pred in self.graph.predecessors(nodes_to_fuse[0]):
            self.graph.add_edge(pred, new_node_name)

        # Connect successors of the last node to the fused node
        for succ in self.graph.successors(nodes_to_fuse[-1]):
            self.graph.add_edge(new_node_name, succ)

        # Remove the fused nodes
        for node in nodes_to_fuse:
            self.graph.remove_node(node)
