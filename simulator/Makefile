CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
SRC_DIR = src
OBJ_DIR = build

SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))

BIN_CLUSTER = $(OBJ_DIR)/core_cluster
BIN_SIMULATOR = $(OBJ_DIR)/simulator

all: $(BIN_CLUSTER)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

$(BIN_CLUSTER): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -rf $(OBJ_DIR)/*.o $(BIN_CLUSTER) $(BIN_SIMULATOR)
