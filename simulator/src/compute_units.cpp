#include "compute_units.hpp"

int CIMUnit::mvm(int weight, int input) {
    return weight * input;  // Simplified placeholder logic
}

int VectorUnit::add(int a, int b) {
    return a + b;
}

int VectorUnit::relu(int a) {
    return (a > 0) ? a : 0;
}

int ScalarUnit::addi(int a, int imm) {
    return a + imm;
}
