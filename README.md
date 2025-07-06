# CIMFlow Framework

**CIMFlow** is a research-grade **compiler-simulator framework** for modeling neural network inference on Compute-In-Memory (CIM) hardware accelerators. It supports multi-core simulation, IR/ISA generation, performance evaluation, and energy modeling.

---

## 🧠 Project Overview

This framework takes a deep learning model (e.g., ResNet18 in ONNX format), compiles it into low-level instruction sets (ISA), and simulates execution on a CIM hardware model to measure cycles, energy, and performance.

---

## 🚀 Features

- ✅ ONNX Model Graph Parsing
- ✅ Stage-Based Partitioning (ResNet Stages)
- ✅ Intermediate Representation (IR) Generation
- ✅ Loop Tiling & ISA Encoding
- ✅ Per-Core Simulation with Tensor Routing
- ✅ Multi-Core Execution Controller
- ✅ Performance Logging (Cycles, Ops)
- ✅ Energy & Latency Estimation
- ✅ Tensor I/O Handling (Inputs & Outputs)

---

## 🛠️ Technologies Used

| Layer              | Tools / Languages                           |
|--------------------|---------------------------------------------|
| **Frontend**       | ONNX Python APIs                            |
| **Compiler**       | Python (Graph Builder, Optimizer, IR/ISA)   |
| **Simulator**      | C++17 (Core, Memory, Perf, ISA Decoder)     |
| **Input Models**   | ResNet18 (ONNX format)                      |
| **Data Format**    | JSON for tensors, logs, and outputs         |
---
Note:- It works on ubuntu OS only.
## ⚙️ How to Run

### Step 1: Install Python Dependencies
```markdown
pip install onnx networkx numpy
```


### Step 2: Build the Simulator:
```markdown
cd simulator
make
cd ..
```


### Step 3: Run the CIMFlow Pipeline
```markdown
python main.py
```
---
## 📊 Output & Logs
### After execution:

#### outputs/ir_dump/ 
 - Per-core IR files

#### outputs/ir_tiled/ 
 - Tiled IRs (loop unrolled)

#### outputs/isa_bin/ 
 - Encoded ISA files

#### outputs/tensor_inputs/ 
 - Auto-generated input tensors

#### logs/
 - Per-core outputs and performance logs

#### logs/core_summary.txt 
 - Aggregated performance report (cycles, energy)
---
## 👨‍🔬 Research Use Case
#### This framework mimics real-world CIM-based NPU behavior, helping evaluate:

- Operator mapping strategies

- Instruction scheduling

- Energy-efficiency

- Partitioning granularity

---
## 🤝 Contributions
Feel free to fork and adapt for your own CIM/NPU designs. Contributions to improve accuracy or simulate analog noise, SRAM variability, or compiler optimizations are welcome.

---
## 📜 License
This project is for academic and research purposes only.
