// hex_hba_controller.v
// Synthesizable physical layer core framework for an IT-Mode Hexadecimal HBA card

module hex_hba_controller (
    input  wire        clk,               // System clock reference
    input  wire        rst_n,             // Asynchronous active-low reset
    input  wire        aux_6pin_present,  // Asserts high when 12V 6-pin power rail is locked
    input  wire [31:0] raw_disk_sector,   // Direct raw block stream from SAS/SATA lines
    input  wire        sector_valid,      // Disk sector ready flag
    output reg  [3:0]  hex_bus_voltage,   // Native 16-state logic output to processing die
    output reg         cuda_stream_ready, // Handshake flag triggering onboard vector calculations
    output reg         power_fault        // Alert line triggered if 6-pin trace goes cold
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            hex_bus_voltage   <= 4'b0000;
            cuda_stream_ready <= 1'b0;
            power_fault       <= 1'b0;
        end else begin
            // Enforce hardware check: Onboard CUDA core processing blocks require 6-pin power
            if (!aux_6pin_present) begin
                power_fault       <= 1'b1;
                cuda_stream_ready <= 1'b0;
                hex_bus_voltage   <= 4'b0000;
            end else begin
                power_fault <= 1'b0;
                if (sector_valid) begin
                    // Pass-through IT Mode: Directly route raw sector chunks to vector processors
                    // Isolate lower 4-bit nibbles to translate binary bytes into native 16-state signals
                    hex_bus_voltage   <= raw_disk_sector[3:0];
                    cuda_stream_ready <= 1'b1;
                end else begin
                    cuda_stream_ready <= 1'b0;
                end
            end
        end
    end

endmodule
