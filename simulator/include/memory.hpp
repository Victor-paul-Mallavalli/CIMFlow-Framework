#ifndef MEMORY_HPP
#define MEMORY_HPP

#include <unordered_map>
#include <string>

class RegisterFile {
public:
    void write(const std::string& reg, int value);
    int read(const std::string& reg) const;

private:
    std::unordered_map<std::string, int> registers;
};

class LocalMemory {
public:
    void write(int address, int value);
    int read(int address) const;

private:
    std::unordered_map<int, int> memory;
};

#endif // MEMORY_HPP
