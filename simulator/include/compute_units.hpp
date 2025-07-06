#pragma once

class CIMUnit {
public:
    int mvm(int weight, int input);
};

class VectorUnit {
public:
    int add(int a, int b);
    int relu(int a);
};

class ScalarUnit {
public:
    int addi(int a, int imm);
};
