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
    // Internal Hex Controller Status
    output reg sec_unlocked,
    output reg [15:0] analog_voltage_mask
);

    // Sega Security System Style Registers
    reg [31:0] hx_security_key;
    reg [31:0] hx_challenge_seed;
    
    localparam ADDR_CHALLENGE = 12'h000;
    localparam ADDR_AUTH_KEY  = 12'h004;
    localparam ADDR_HEX_DATA  = 12'h008;
    
    always @(posedk clk or negedge rst_n) begin
        if (!rst_n) begin
            hx_security_key    <= 32'h0;
            hx_challenge_seed  <= 32'hA5A55A5A; // Static boot seed
            sec_unlocked       <= 1'b0;
            analog_voltage_mask<= 16'h0000; // Complete suppression
            pcie_rdata         <= 32'h0;
        end else begin
            if (pcie_write) begin
                case (pcie_addr)
                    ADDR_AUTH_KEY: begin
                        hx_security_key <= pcie_wdata;
                        // Sega style simple validation check: key must match transformed challenge
                        if (pcie_wdata == (hx_challenge_seed ^ 32'h5E6A5ECE)) begin
                            sec_unlocked <= 1'b1;
                            analog_voltage_mask <= 16'hFFFF; // Enable all 16 states
                        end else begin
                            sec_unlocked <= 1'b0;
                            analog_voltage_mask <= 16'h0000; // Clamp system voltage
                        end
                    end
                    default: begin
                        // Discard writes if locked
                    end
                endcase
            end else begin
                // Read operations
                case (pcie_addr)
                    ADDR_CHALLENGE: pcie_rdata <= hx_challenge_seed;
                    ADDR_HEX_DATA:  pcie_rdata <= (sec_unlocked) ? 32'h1657A7E1 : 32'hDEADBEEF;
                    default:        pcie_rdata <= 32'h0;
                endcase
            end
        end
    end
endmodule
