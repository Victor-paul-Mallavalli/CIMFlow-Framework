#ifndef PERF_COUNTER_HPP
#define PERF_COUNTER_HPP

#include <unordered_map>
#include <string>

class PerfCounter {
private:
    int total_cycles = 0;
    std::unordered_map<std::string, int> unit_usage;

public:
    void count(const std::string& unit);

    void tick();

    void report() const;

    void report_to_file(const std::string& filename) const;

    void report_energy_to_file(const std::string& filename) const;
};

#endif 
