// File: hardware/chassis_assembly.scad
/**
 * Revolutionary Technology (RT) Architecture - Chassis Assembly Blueprint
 * Integrates the RT-TOUGHAIR-16X Dual-Tower CPU Cooler Volume Clearances.
 * All dimensions specified in millimeters (mm).
 */

$fn = 60; // Set render circular detail resolution

// --- Core Mechanical Dimensions ---
motherboard_w  = 305;  // Standard width
motherboard_d  = 244;  // Standard depth
board_thick    = 2.4;  // 8-layer high-density PCB depth
chassis_wall   = 4.0;  // Reinforced structural frame wall thickness
interior_h     = 195;  // Increased vertical height to clear the 165mm dual-tower cooler!

// --- Footprint Spatial Offsets ---
camm2_offset   = [45,  160, board_thick];
optical_offset = [160, 40,  board_thick];
satcom_offset  = [20,  40,  board_thick];
cpu_offset     = [110, 100, board_thick]; // Target CPU location

module motherboard_base() {
    color("DarkGreen") {
        cube([motherboard_w, motherboard_d, board_thick]);
    }
    
    // CPU Core 1 Component Positioning Block
    color("LightGray") {
        translate([cpu_offset[0], cpu_offset[1], cpu_offset[2]])
            cube([55, 55, 4.5]); // Native Hex-BGA form factor
    }
}

module rt_toughair_16x_clearance() {
    // Custom Dual-Tower Heatsink Assembly inspired by Thermaltake TOUGHAIR 710
    // Total footprint: 148.5mm wide, 146.6mm deep, 165mm vertical height clearance
    translate([cpu_offset[0] - 46, cpu_offset[1] - 45, cpu_offset[2] + 4.5]) {
        
        // Tower 1: Front Aluminum Fin Stack
        color("Silver", 0.9) {
            cube([148.5, 45, 160]);
        }
        
        // Nested Mid-Fan: Center static-pressure blower array
        color("DimGray", 0.9) {
            translate([0, 53, 0])
                cube([140, 25, 140]);
        }
        
        // Tower 2: Rear Aluminum Fin Stack
        color("Silver", 0.9) {
            translate([0, 85, 0])
                cube([148.5, 45, 160]);
        }
        
        // Outer Fan: Front pull blower array (Adjustable up to 23mm vertical slide for CAMM2 clearance)
        color("DimGray", 0.9) {
            translate([4.25, -28, 23]) // Lifted 23mm to completely bypass tall memory modules
                cube([140, 25, 140]);
        }
    }
}

module camm2_socket_clearance() { color("DimGray") { cube([78, 64, 6.0]); } }
module optoelectronic_card_clearance() { color("RoyalBlue") { cube([110, 85, 22.0]); } }
module satcom_pcie_card_clearance() { color("Gold") { cube([140, 18, 45.0]); } }

module chassis_shell() {
    ext_w = motherboard_w + (chassis_wall * 2) + 10;
    ext_d = motherboard_d + (chassis_wall * 2) + 10;
    ext_h = interior_h + chassis_wall + board_thick;

    difference() {
        color("SlateGray", 0.4) { // Increased transparency to audit internal tower alignment
            translate([-chassis_wall - 5, -chassis_wall - 5, -chassis_wall])
                cube([ext_w, ext_d, ext_h]);
        }
        translate([-5, -5, 0])
            cube([motherboard_w + 10, motherboard_d + 10, interior_h + 10]);
            
        // Exhaust openings matching the dual tower airflow path
        for(i = [0 : 25 : motherboard_w - 20]) {
            translate([i, motherboard_d + chassis_wall, interior_h / 2])
                rotate([90, 0, 0])
                    cylinder(h = chassis_wall + 15, r = 6.5, center = true);
        }
    }
}

module assemble_chassis_workspace() {
    chassis_shell();
    motherboard_base();
    
    // Mount the dual-tower cooling structure directly over the processor substrate
    rt_toughair_16x_clearance();
    
    translate(camm2_offset) camm2_socket_clearance();
    translate(optical_offset) optoelectronic_card_clearance();
    translate(satcom_offset) satcom_pcie_card_clearance();
}

assemble_chassis_workspace();
