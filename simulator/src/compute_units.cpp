#include "compute_units.hpp"

// CIM Unit: Simulated Matrix-Vector Multiplication
int CIMUnit::mvm(int weight, int input) {
    return weight * input;  // Simplified placeholder logic
}

// Vector Unit: Element-wise operations
int VectorUnit::add(int a, int b) {
    return a + b;
}

int VectorUnit::relu(int a) {
    return (a > 0) ? a : 0;
}

// Scalar Unit: Immediate arithmetic
int ScalarUnit::addi(int a, int imm) {
    return a + imm;
}