#include "perf_counter.hpp"
#include <iostream>
#include <fstream>
#include <map>

void PerfCounter::count(const std::string& unit) {
    unit_usage[unit]++;
}

void PerfCounter::tick() {
    total_cycles++;
}

void PerfCounter::report() const {
    std::cout << "\n=== Performance Report ===\n";
    std::cout << "Total Cycles: " << total_cycles << "\n";
    for (const auto& [unit, count] : unit_usage) {
        std::cout << unit << " Usage: " << count << "\n";
    }
    std::cout << "==========================\n";
}

void PerfCounter::report_to_file(const std::string& filename) const {
    std::ofstream out(filename);
    if (!out) return;

    out << "=== Performance Report ===\n";
    out << "Total Cycles: " << total_cycles << "\n";
    for (const auto& [unit, count] : unit_usage) {
        out << unit << " Usage: " << count << "\n";
    }
    out << "==========================\n";
}

void PerfCounter::report_energy_to_file(const std::string& filename) const {
    std::map<std::string, double> energy_per_op = {
        {"CIM", 1.5},    // picojoules
        {"VEC", 0.6},
        {"SCALAR", 0.2}
    };

    std::ofstream out(filename);
    if (!out) return;

    out << "=== Energy Report ===\n";
    double total_energy = 0.0;

    for (const auto& [unit, count] : unit_usage) {
        double energy = count * energy_per_op[unit];
        out << unit << " Energy: " << energy << " pJ\n";
        total_energy += energy;
    }

    out << "----------------------\n";
    out << "Total Energy: " << total_energy << " pJ\n";
    out << "=======================\n";
}
