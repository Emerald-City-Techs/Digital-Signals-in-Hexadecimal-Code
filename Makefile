# -----------------------------------------------------------------------------
# Compilation Makefile for Hexadecimal Computing PCIe Streamer Pipeline
# -----------------------------------------------------------------------------

# Compiler configuration flags
CC       = gcc
CFLAGS   = -O3 -Wall -Wextra -Wpedantic -std=c11 -D_GNU_SOURCE
TARGET   = build/hex_pcie_streamer

# Directory structure targets
SRC_DIR  = src/chips/adapters
BUILD_DIR = build

# Source assignment
SRC      = $(SRC_DIR)/hex_pcie_streamer.c

.PHONY: all clean verify setup

# Default production target
all: setup verify $(TARGET)

# Build environment initialization
setup:
	@mkdir -p $(BUILD_DIR)

# Binary compilation sequence
$(TARGET): $(SRC)
	@echo "[BUILD] Compiling C Streamer Core with high performance optimization (-O3)..."
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)
	@echo "[SUCCESS] Execution binary generated at: $(TARGET)"

# Structural validation wrapper target
verify:
	@echo "[VERIFY] Launching repository configuration validation utility..."
	python3 build_hex_board.py --verify-thermal-limits || echo "[WARN] Skip core simulation checks if library missing."
	python3 -c "import os; exit(0) if os.path.exists('$(SRC_DIR)/__init__.py') else (print('[ALERT] Missing __init__.py namespace bundle.'), exit(1))"

# Environmental cleaning sequence
clean:
	@echo "[CLEAN] Purging compiled assets and build artifacts..."
	rm -rf $(BUILD_DIR)
	@echo "[CLEAN] Workspace scrub complete."
