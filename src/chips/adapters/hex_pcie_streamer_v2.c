#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define HEX_PCIE_BAR0_BASE     0x40000000  // Memory-Mapped I/O Base Anchor
#define PHY_DATA_REG_OFFSET    0x00001000  // Data write register offset
#define PHY_STATUS_REG_OFFSET  0x00001004  // Status register offset (contains ready bit)

#define PHY_READY_MASK         (1X0 << 0)   // Bit 0 tracks Verilog phy_tx_ready status
#define TRANSMIT_TIMEOUT_COUNT 100000      // Maximum hardware loop retries

// Volatile pointers to prevent compiler optimization of hardware register access
volatile uint32_t* const pcie_phy_data   = (volatile uint32_t*)(HEX_PCIE_BAR0_BASE + PHY_DATA_REG_OFFSET);
volatile uint32_t* const pcie_phy_status = (volatile uint32_t*)(HEX_PCIE_BAR0_BASE + PHY_STATUS_REG_OFFSET);

/**
 * Transmits a 4-bit hexadecimal token with hardware ready status verification.
 * Returns true if successful, false if a hardware timeout occurs.
 */
bool write_hardware_nibble_with_timeout(uint8_t nibble) {
    uint32_t timeout_counter = 0;

    // Poll the status register until the Verilog PHY signals ready
    while (((*pcie_phy_status) & PHY_READY_MASK) == 0) {
        timeout_counter++;
        if (timeout_counter >= TRANSMIT_TIMEOUT_COUNT) {
            fprintf(stderr, "[ERROR] PHY transmission timeout! phy_tx_ready failed to assert high.\n");
            return false;
        }
    }

    // Mask payload to prevent signaling trace boundary leakage
    uint32_t output_payload = (uint32_t)(nibble & 0x0F);
    
    // Commit direct write across physical controller pipeline bus
    *pcie_phy_data = output_payload;
    return true;
}

/**
 * Parses and streams a sequential byte array over the hexadecimal analog layer.
 * Aborts early and logs status if an endpoint timeout error occurs.
 */
bool stream_sequential_buffer(const uint8_t* data_buffer, size_t buffer_length) {
    if (data_buffer == NULL || buffer_length == 0) {
        return false;
    }

    printf("[STREAMER] Beginning block transaction of size: %zu bytes.\n", buffer_length);

    for (size_t i = 0; i < buffer_length; i++) {
        uint8_t tracking_byte = data_buffer[i];

        // 1. Isolate and dispatch High Order Nibble (Bits 7-4)
        uint8_t upper_nibble = (tracking_byte >> 4) & 0x0F;
        if (!write_hardware_nibble_with_timeout(upper_nibble)) {
            fprintf(stderr, "[STREAMER] Fatal link error at buffer index %zu (Upper Nibble).\n", i);
            return false;
        }

        // 2. Isolate and dispatch Low Order Nibble (Bits 3-0)
        uint8_t lower_nibble = tracking_byte & 0x0F;
        if (!write_hardware_nibble_with_timeout(lower_nibble)) {
            fprintf(stderr, "[STREAMER] Fatal link error at buffer index %zu (Lower Nibble).\n", i);
            return false;
        }
    }

    printf("[STREAMER] Sequenced buffer successfully committed to endpoint hardware.\n");
    return true;
}

int main(void) {
    uint8_t target_payload[] = { 0x5A, 0xFF, 0x01, 0x8B };

    if (!stream_sequential_buffer(target_payload, sizeof(target_payload))) {
        fprintf(stderr, "[SYSTEM] Critical: Streaming pipeline failed during runtime.\n");
        return 1;
    }

    return 0;
}
