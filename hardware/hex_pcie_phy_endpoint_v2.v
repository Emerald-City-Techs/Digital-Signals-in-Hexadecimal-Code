// File: hardware/hex_pcie_phy_endpoint.v
`timescale 1ns / 1ps

module hex_pcie_phy_endpoint (
    input wire clk,
    input wire rst_n,
    
    // PCIe Bus Interface
    input wire [31:0] pcie_wdata,
    input wire [11:0] pcie_addr,
    input wire pcie_write,
    output reg [31:0] pcie_rdata,
    
    // Physical Silicon Interfaces
    output reg sec_unlocked,
    output reg [15:0] analog_voltage_mask, // Controls which voltage steps are active
    
    // 16-State Input/Output Signal Interfaces
    input wire [3:0] logical_hex_in,
    output reg [3:0] obfuscated_voltage_out
);

    // Sega Security System Style Registers
    reg [31:0] hx_security_key;
    reg [31:0] hx_challenge_seed;
    
    // 16-State Dynamic Obfuscation Look-Up Table (LUT)
    // 16 entries, each 4-bits wide, mapping a logical nibble to a physical voltage step index
    reg [3:0] obfuscation_lut [0:15];
    integer i;

    // Memory-Mapped Address Aliases
    localparam ADDR_CHALLENGE = 12'h000;
    localparam ADDR_AUTH_KEY  = 12'h004;
    localparam ADDR_HEX_DATA  = 12'h008;
    
    // Combinational or Sequential Signal Mapping Routing
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            obfuscated_voltage_out <= 4'h0;
        end else if (sec_unlocked) begin
            // Dynamic routing through the shuffled lookup table
            obfuscated_voltage_out <= obfuscation_lut[logical_hex_in];
        end else begin
            // Hardware Lockout: Clamp all outgoing signals to ground (0.0V state)
            obfuscated_voltage_out <= 4'h0;
        end
    end

    // Bus Registers Control Loop & Shuffling Execution
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            hx_security_key     <= 32'h0;
            hx_challenge_seed   <= 32'hA5A55A5A; // Hardware boot seed
            sec_unlocked        <= 1'b0;
            analog_voltage_mask <= 16'h0000;     // Lockout state: clear all lines
            pcie_rdata          <= 32'h0;
            
            // Default linear mapping state before unlock
            for (i = 0; i < 16; i = i + 1) begin
                obfuscation_lut[i] <= i[3:0];
            end
        end else begin
            if (pcie_write) begin
                case (pcie_addr)
                    ADDR_AUTH_KEY: begin
                        hx_security_key <= pcie_wdata;
                        
                        // Sega FD1094 style block verification mapping
                        if (pcie_wdata == (hx_challenge_seed ^ 32'h5E6A5ECE)) begin
                            sec_unlocked        <= 1'b1;
                            analog_voltage_mask <= 16'hFFFF; // Open voltage gates
                            
                            // Deterministically shuffle the lookup table based on bits of the valid key.
                            // This creates a unique physical voltage profile per session/key.
                            obfuscation_lut[4'h0] <= pcie_wdata[3:0];
                            obfuscation_lut[4'h1] <= pcie_wdata[7:4];
                            obfuscation_lut[4'h2] <= pcie_wdata[11:8];
                            obfuscation_lut[4'h3] <= pcie_wdata[15:12];
                            obfuscation_lut[4'h4] <= pcie_wdata[19:16];
                            obfuscation_lut[4'h5] <= pcie_wdata[23:20];
                            obfuscation_lut[4'h6] <= pcie_wdata[27:24];
                            obfuscation_lut[4'h7] <= pcie_wdata[31:28];
                            
                            // Complementary inversion mapping for the upper banks
                            obfuscation_lut[4'h8]  <= ~pcie_wdata[3:0];
                            obfuscation_lut[4'h9]  <= ~pcie_wdata[7:4];
                            obfuscation_lut[4'hA]  <= ~pcie_wdata[11:8];
                            obfuscation_lut[4'hB]  <= ~pcie_wdata[15:12];
                            obfuscation_lut[4'hC]  <= ~pcie_wdata[19:16];
                            obfuscation_lut[4'hD]  <= ~pcie_wdata[23:20];
                            obfuscation_lut[4'hE]  <= ~pcie_wdata[27:24];
                            obfuscation_lut[4'hF]  <= ~pcie_wdata[31:28];
                        end else begin
                            // Tamper Lockout Action
                            sec_unlocked        <= 1'b0;
                            analog_voltage_mask <= 16'h0000;
                            for (i = 0; i < 16; i = i + 1) begin
                                obfuscation_lut[i] <= 4'h0; // Flush data routing tables
                            end
                        end
                    end
                    default: begin
                        // Silently drop writes to protected addresses when locked
                    end
                endcase
            end else begin
                // Host Read Interface Execution
                case (pcie_addr)
                    ADDR_CHALLENGE: pcie_rdata <= hx_challenge_seed;
                    ADDR_HEX_DATA:  pcie_rdata <= (sec_unlocked) ? 32'h1657A7E1 : 32'hDEADBEEF;
                    default:        pcie_rdata <= 32'h0;
                endcase
            end
        end
    end
endmodule
