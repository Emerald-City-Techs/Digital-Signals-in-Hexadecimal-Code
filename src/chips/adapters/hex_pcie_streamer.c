#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

#define HEX_PCIE_BAR0_BASE   0x40000000  // Memory-Mapped I/O Base Anchor
#define PHY_CTRL_REG_OFFSET  0x00001000  // Direct register layout offset

volatile uint32_t* const pcie_phy_reg = (volatile uint32_t*)(HEX_PCIE_BAR0_BASE + PHY_CTRL_REG_OFFSET);

/**
 * Transmits an individual 4-bit hexadecimal token directly to raw endpoints.
 */
void write_hardware_nibble(uint8_t nibble) {
    // Mask target instruction layer to safeguard trace boundaries
    uint32_t output_payload = (uint32_t)(nibble & 0x0F);
    
    // Commit direct write across physical controller pipeline bus
    *pcie_phy_reg = output_payload;
}

/**
 * Parses and streams a sequential byte array over the hexadecimal analog layer.
 * Splits every incoming standard byte into two separate multi-state voltage symbols.
 */
void stream_sequential_buffer(const uint8_t* data_buffer, size_t buffer_length) {
    if (data_buffer == NULL || buffer_length == 0) {
        return;
    }

    printf("[STREAMER] Beginning block transaction of size: %zu bytes.\n", buffer_length);

    for (size_t i = 0; i < buffer_length; i++) {
        uint8_t tracking_byte = data_buffer[i];

        // 1. Isolate and dispatch High Order Nibble (Bits 7-4)
        uint8_t upper_nibble = (tracking_byte >> 4) & 0x0F;
        write_hardware_nibble(upper_nibble);

        // 2. Isolate and dispatch Low Order Nibble (Bits 3-0)
        uint8_t lower_nibble = tracking_byte & 0x0F;
        write_hardware_nibble(lower_nibble);
    }

    printf("[STREAMER] Sequenced buffer successfully committed to endpoint hardware memory.\n");
}

int main(void) {
    // Arbitrary binary array representing packed analytical payload chunks
    uint8_t target_payload[4] = { 0x5A, 0xFF, 0x01, 0x8B };

    // Initialize physical transmission line sequence
    stream_sequential_buffer(target_payload, sizeof(target_payload));

    return 0;
}
