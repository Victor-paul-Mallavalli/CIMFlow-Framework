#ifndef PERF_COUNTER_HPP
#define PERF_COUNTER_HPP

#include <unordered_map>
#include <string>

class PerfCounter {
private:
    int total_cycles = 0;
    std::unordered_map<std::string, int> unit_usage;

public:
    // Increments the usage count of a specific compute unit (e.g., "CIM", "VEC")
    void count(const std::string& unit);

    // Increments the global cycle counter
    void tick();

    // Prints a performance report to stdout
    void report() const;

    // Saves a performance report to a log file
    void report_to_file(const std::string& filename) const;

    // Saves an energy estimation report to a log file
    void report_energy_to_file(const std::string& filename) const;
};

#endif // PERF_COUNTER_HPP
