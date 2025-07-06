#include "memory.hpp"

void RegisterFile::write(const std::string& reg, int value) {
    registers[reg] = value;
}

int RegisterFile::read(const std::string& reg) const {
    auto it = registers.find(reg);
    return it != registers.end() ? it->second : 0;
}

void LocalMemory::write(int address, int value) {
    memory[address] = value;
}

int LocalMemory::read(int address) const {
    auto it = memory.find(address);
    return it != memory.end() ? it->second : 0;
}
