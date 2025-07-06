#ifndef CORE_HPP
#define CORE_HPP

#include <string>
#include <vector>
#include <unordered_map>
#include "memory.hpp"
#include "perf_counter.hpp"
//#include "utils.hpp"
#include "compute_units.hpp"  // Define CIMUnit, VecUnit, ScalarUnit here

class Core {
public:
    Core(const std::string& isa_path);

    // Set input tensor file path (e.g., from IR dump)
    void set_input_tensor_path(const std::string& path);

    // Load .isa into instruction buffer
    void load_instructions();

    // Load JSON tensor input
    void load_tensor_mem(const std::string& path);

    // Save output JSON
    void save_tensor_mem(const std::string& path);

    // Run full decode-execute loop
    void run(const std::string& log_file, const std::string& output_file);

private:
    std::string isa_path;
    std::string input_tensor_path;

    std::vector<std::string> instructions;
    std::unordered_map<std::string, std::vector<int>> tensor_mem;

    // Compute and memory subsystems
    RegisterFile regs;
    LocalMemory local_mem;
    PerfCounter perf;

    CIMUnit cim;
    VectorUnit vec;  
    ScalarUnit scalar;

    void decode(const std::string& inst);
    void execute(const std::string& opcode, const std::vector<std::string>& operands, const std::string& output_tensor);
};

#endif 
