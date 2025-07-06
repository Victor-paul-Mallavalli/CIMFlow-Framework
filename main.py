import os
from compiler.graph_builder import ComputationGraph
from compiler.cg_optimizer import CGOptimizer
from compiler.ir_generator import IRGenerator
from compiler.isa_encoder import ISAEncoder
from compiler.op_optimizer import OperatorOptimizer
from utils.config import load_arch_config
import subprocess

def run_cimflow_pipeline(onnx_model_path, config_path="config/arch_config.json"):
    print("\n [CIMFlow] Starting Compiler-Simulator Pipeline")

    # Step 1: Load Hardware Configuration
    config = load_arch_config(config_path)

    # Step 2: Build Computation Graph
    print("\n Building computation graph...")
    cg = ComputationGraph(onnx_model_path)
    graph = cg.build_graph()

    # Step 3: Partition using Stage-Based Strategy
    print("\n Partitioning with stage-based strategy...")
    optimizer = CGOptimizer(graph, config, use_stage_partition=True)
    partitions, partition_map = optimizer.dynamic_partition()
    optimizer.print_partitions()

    # Step 4: IR Generation
    print("\n Generating IR files...")
    irgen = IRGenerator(graph, partition_map)
    irgen.generate_ir()

    # Step 5: Optimize Operators
    print("\n Optimizing operators per partition...")
    op = OperatorOptimizer(ir_dir="outputs/ir_dump", output_dir="outputs/ir_tiled")
    op.optimize()

    # Step 6: ISA Encoding
    print("\n Encoding ISA files...")
    encoder = ISAEncoder(graph,ir_dir="outputs/ir_tiled", output_dir="outputs/isa_bin")
    encoder.encode_all()

    # Step 7: Tensor Input Generation
    print("\n Generating input tensors for simulation...")
    subprocess.run(["python3", "compiler/generate_tensor_inputs.py"])

    # Step 8: Build and Launch Multi-Core Simulator
    print("\n Launching multi-core simulator...")
    os.chdir("simulator")
    subprocess.run(["make"])
    subprocess.run(["./build/core_cluster", "../outputs/isa_bin", "../logs"])

    # Step 9: Summary of each core and aggregation of cores
    os.chdir("../")
    subprocess.run(["python3", "generate_core_summary.py"])

    print("\n CIMFlow pipeline completed successfully.")

if __name__ == "__main__":
    MODEL_PATH = "models/resnet18.onnx"
    run_cimflow_pipeline(MODEL_PATH)
