#include "core.hpp"
#include <filesystem>
#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <nlohmann/json.hpp>
#include <thread>
#include <mutex>

using json = nlohmann::json;
namespace fs = std::filesystem;

std::mutex global_tensor_mem_mutex;

void process_core(const fs::path& isa_path, int core_id, const std::string& log_dir, const std::string& tensor_dir, std::map<std::string, std::vector<int>>& global_tensor_mem) {
    std::string isa_file = isa_path.string();
    std::string output_file = log_dir + "/core_" + std::to_string(core_id) + "_output.json";
    std::string perf_file   = log_dir + "/core_" + std::to_string(core_id) + "_perf.txt";
    std::string tensor_input_file = tensor_dir + "/tensor_input_" + std::to_string(core_id) + ".json";

    std::cout << "\nLaunching Core " << core_id << " → " << isa_file << "\n";

    Core core(isa_file);

    if (fs::exists(tensor_input_file)) {
        core.set_input_tensor_path(tensor_input_file);
        std::cout << "Using input tensor: " << tensor_input_file << "\n";
    } else {
        std::cerr << "Tensor input file not found for core " << core_id << ": " << tensor_input_file << "\n";
    }

    core.load_instructions();
    core.run(perf_file, output_file);

    std::ifstream result(output_file);
    if (result.is_open()) {
        json j;
        result >> j;
        std::lock_guard<std::mutex> lock(global_tensor_mem_mutex);
        for (auto& [k, v] : j.items()) {
            global_tensor_mem[k] = v.get<std::vector<int>>();
        }
    }
}

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "Usage: ./core_cluster <isa_dir> <log_dir>\n";
        return 1;
    }

    std::string isa_dir = argv[1];
    std::string log_dir = argv[2];
    std::string tensor_dir = "../outputs/tensor_inputs";

    fs::create_directories(log_dir);
    std::map<std::string, std::vector<int>> global_tensor_mem;

    std::vector<fs::path> isa_files;
    for (const auto& entry : fs::directory_iterator(isa_dir)) {
        if (entry.path().extension() == ".isa")
            isa_files.push_back(entry.path());
    }
    std::sort(isa_files.begin(), isa_files.end());

    std::vector<std::thread> threads;
    int core_id = 0;

    for (const auto& isa_path : isa_files) {
        threads.emplace_back(process_core, isa_path, core_id, log_dir, tensor_dir, std::ref(global_tensor_mem));
        core_id++;
    }

    for (auto& thread : threads) {
        thread.join();
    }

    std::cout << "\nMulti-core simulation completed.\n";
    return 0;
}
