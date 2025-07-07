#include "core.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

Core::Core(const std::string& path) : isa_path(path) {}

void Core::set_input_tensor_path(const std::string& path) {
    input_tensor_path = path;
}

void Core::load_instructions() {
    std::ifstream file(isa_path);
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty() && line[0] != '#')
            instructions.push_back(line);
    }
}

void Core::load_tensor_mem(const std::string& path) {
    std::ifstream in(path);
    if (!in.is_open()) {
        std::cerr << "Could not open input tensor file: " << path << "\n";
        return;
    }

    json j;
    in >> j;
    for (auto& [key, value] : j.items()) {
        tensor_mem[key] = value.get<std::vector<int>>();
    }

    std::cout << "Loaded input tensor from " << path << "\n";
    for (const auto& [k, v] : tensor_mem) {
        std::cout << "  " << k << ": ";
        for (int x : v) std::cout << x << " ";
        std::cout << "\n";
    }
}

void Core::save_tensor_mem(const std::string& path) {
    json j;
    for (const auto& [name, vec] : tensor_mem) {
        j[name] = vec;
    }
    std::ofstream out(path);
    out << j.dump(4);
}

void Core::run(const std::string& log_file, const std::string& output_file) {
    load_tensor_mem(input_tensor_path);

    for (const std::string& inst : instructions) {
        decode(inst);
        perf.tick();
    }

    perf.report();
    perf.report_to_file(log_file);
    save_tensor_mem(output_file);
    std::cout << "Saved output tensor to " << output_file << "\n";
}

void Core::decode(const std::string& inst) {
    std::istringstream iss(inst);
    std::string opcode;
    iss >> opcode;

    std::vector<std::string> operands;
    std::string op;

    while (iss >> op) {
        if (op == "//") break;
        if (!op.empty() && op.back() == ',') op.pop_back();
        operands.push_back(op);
    }

    std::string comment;
    std::getline(iss, comment);
    std::string output_tensor = operands.size() > 2 ? operands[2] : "R3"; 

    size_t pos = comment.find_first_not_of(" /");
    if (!comment.empty() && pos != std::string::npos) {
        output_tensor = comment.substr(pos);
    }

    execute(opcode, operands, output_tensor);
}

void Core::execute(const std::string& opcode, const std::vector<std::string>& operands, const std::string& output_tensor) {
    std::cout << "[EXEC] " << opcode;
    for (const std::string& o : operands) std::cout << " " << o;
    std::cout << " // " << output_tensor << "\n";

    if (opcode == "VEC_ADD") {
        perf.count("VEC");

        if (operands.size() < 2 || tensor_mem.find(operands[0]) == tensor_mem.end() || tensor_mem.find(operands[1]) == tensor_mem.end()) {
            std::cerr << "Missing operands for VEC_ADD\n";
            return;
        }

        const auto& a = tensor_mem[operands[0]];
        const auto& b = tensor_mem[operands[1]];

        if (a.size() != b.size()) {
            std::cerr << "VEC_ADD size mismatch: " << operands[0] << " (" << a.size() << ") vs " << operands[1] << " (" << b.size() << ")\n";
        }

        std::vector<int> result;
        for (size_t i = 0; i < std::min(a.size(), b.size()); ++i)
            result.push_back(vec.add(a[i], b[i]));

        tensor_mem[output_tensor] = result;
    }

    else if (opcode == "VEC_RELU") {
        perf.count("VEC");

        if (operands.empty() || tensor_mem.find(operands[0]) == tensor_mem.end()) {
            std::cerr << "Missing operand for VEC_RELU\n";
            return;
        }

        const auto& a = tensor_mem[operands[0]];
        std::vector<int> result;
        for (int val : a)
            result.push_back(vec.relu(val));

        tensor_mem[output_tensor] = result;
    }

    else if (opcode == "CIM_MVM") {
        perf.count("CIM");

        if (operands.size() < 2 || tensor_mem.find(operands[0]) == tensor_mem.end() || tensor_mem.find(operands[1]) == tensor_mem.end()) {
            std::cerr << "Missing operands for CIM_MVM\n";
            return;
        }

        const auto& w = tensor_mem[operands[0]];
        const auto& x = tensor_mem[operands[1]];

        if (w.size() != x.size()) {
            std::cerr << "CIM_MVM size mismatch: " << operands[0] << " (" << w.size() << ") vs " << operands[1] << " (" << x.size() << ")\n";
        }

        std::vector<int> result;
        for (size_t i = 0; i < std::min(w.size(), x.size()); ++i)
            result.push_back(cim.mvm(w[i], x[i]));

        tensor_mem[output_tensor] = result;
    }

    else if (opcode == "SC_ADDI") {
        perf.count("SCALAR");
        if (operands.size() < 2) {
            std::cerr << "Invalid SC_ADDI operands\n";
            return;
        }

        int base = regs.read(operands[0]);
        int imm = std::stoi(operands[1]);
        regs.write(output_tensor, scalar.addi(base, imm));
    }

    if (tensor_mem.find(output_tensor) != tensor_mem.end()) {
        std::cout << "Output (" << output_tensor << "): ";
        for (int val : tensor_mem[output_tensor])
            std::cout << val << " ";
        std::cout << "\n";
    } else {
        try {
            int val = regs.read(output_tensor);
            std::cout << "Output (" << output_tensor << "): " << val << "\n";
        } catch (...) {
            std::cout << "Output (" << output_tensor << "): [undefined]\n";
        }
    }
}
