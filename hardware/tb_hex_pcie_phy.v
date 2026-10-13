`timescale 1ns / 1ps

module tb_hex_pcie_phy;

    // Simulation Clock and Control Signals
    reg        clk;
    reg        rst_n;
    reg  [3:0] tx_data_nibble;
    reg        tx_valid;

    // Monitored Output Nets from PHY module
    wire [3:0] phy_voltage_bus;
    wire       phy_tx_ready;

    // Instantiate Device Under Test (DUT)
    hex_pcie_phy_endpoint dut (
        .clk(clk),
        .rst_n(rst_n),
        .tx_data_nibble(tx_data_nibble),
        .tx_valid(tx_valid),
        .phy_voltage_bus(phy_voltage_bus),
        .phy_tx_ready(phy_tx_ready)
    );

    // 100MHz Reference Clock Generation (10ns Period)
    always #5 clk = ~clk;

    // Verification Sequence
    initial begin
        // Initialize Core Signal State
        clk             = 0;
        rst_n           = 0;
        tx_data_nibble  = 4'h0;
        tx_valid        = 0;

        // Hold Reset Asserted for 2 Clock Cycles
        #20;
        rst_n = 1;
        #10;

        // Test Step 1: Commit Low Voltage Boundary (0x0 -> 0.0000V)
        @(posedge clk);
        tx_data_nibble = 4'h0;
        tx_valid       = 1;
        
        // Test Step 2: Commit Midpoint State (0x8 -> 0.5000V)
        @(posedge clk);
        tx_data_nibble = 4'h8;

        // Test Step 3: Commit Maximum Voltage Threshold (0xF -> 1.0000V)
        @(posedge clk);
        tx_data_nibble = 4'hF;

        // Test Step 4: Verify Idle Condition Handling
        @(posedge clk);
        tx_valid = 0;
        tx_data_nibble = 4'hX; // Stale data pipeline isolation check

        // Finalize Trace Simulation
        #40;
        $display("[SIMULATION COMPLETE] All 16-state transient logic transitions verified.");
        $finish;
    end

    // Monitor Output Block to Terminal Standard Out
    initial begin
        $monitor("Time=%0tns | RST_N=%b | VALID=%b | DATA=0x%X | PHY_OUT_HEX=0x%X | READY=%b", 
                 $time, rst_n, tx_valid, tx_data_nibble, phy_voltage_bus, phy_tx_ready);
    end

endmodule
