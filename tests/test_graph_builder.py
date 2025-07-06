# tests/test_graph_builder.py

from compiler.graph_builder import ComputationGraph

def test_graph_construction():
    model_path = "models/resnet18.onnx"
    cg = ComputationGraph(model_path)
    graph = cg.build_graph()

    assert len(graph.nodes) > 0, "Graph has no nodes!"
    assert len(graph.edges) > 0, "Graph has no edges!"

    print("✅ test_graph_construction passed.")
