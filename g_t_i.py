import onnx
import numpy as np
from onnx import numpy_helper

def extract_onnx_inputs_and_initializers(onnx_path, output_path="onnx_tensor_info.txt"):
    model = onnx.load(onnx_path)
    graph = model.graph

    initializer_names = {init.name for init in graph.initializer}

    with open(output_path, "w") as f:
        f.write("📥 Model Inputs (excluding weights):\n\n")
        for input_tensor in graph.input:
            name = input_tensor.name
            shape = [dim.dim_value for dim in input_tensor.type.tensor_type.shape.dim]
            dtype = input_tensor.type.tensor_type.elem_type

            if name not in initializer_names:
                f.write(f"Input Name : {name}\n")
                f.write(f"  Shape    : {shape}\n")
                f.write(f"  Dtype    : {dtype} (ONNX tensor type)\n\n")

        f.write("\n🔐 Initializers (weights/constants):\n\n")
        for init in graph.initializer:
            arr = numpy_helper.to_array(init)
            f.write(f"Initializer Name : {init.name}\n")
            f.write(f"  Shape          : {arr.shape}\n")
            f.write(f"  Dtype          : {arr.dtype}\n")
            f.write(f"  Values         : {arr.flatten().tolist()[:10]}...\n\n")  # Show only first 10 values

    print(f"✅ Tensor information written to {output_path}")

if __name__ == "__main__":
    extract_onnx_inputs_and_initializers("models/resnet18.onnx")
