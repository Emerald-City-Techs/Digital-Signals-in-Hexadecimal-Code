// File: hardware/chassis_assembly.scad
/**
 * Revolutionary Technology (RT) Architecture - Chassis Assembly Blueprint
 * Generates the mechanical mounting boundaries, cooling ports, and card slot alignments.
 * All base metric parameters specified in millimeters (mm).
 */

$fn = 60; // Set render circular detail resolution

// --- Core Mechanical Dimensions ---
motherboard_w  = 305;  // Standard industrial format footprint width
motherboard_d  = 244;  // Standard depth clearance
board_thick    = 2.4;  // Rigid 8-layer high-density PCB depth
chassis_wall   = 4.0;  // Reinforced structural frame wall thickness
interior_h     = 85;   // Total internal vertical layout height

// --- Footprint Spatial Offsets ---
camm2_offset   = [45,  160, board_thick];
optical_offset = [160, 40,  board_thick];
satcom_offset  = [20,  40,  board_thick];

module motherboard_base() {
    // Primary 8-layer structural substrate layout representation
    color("DarkGreen") {
        cube([motherboard_w, motherboard_d, board_thick]);
    }
    
    // Integrated CPU Core 1 Component Positioning Block
    color("LightGray") {
        translate([110, 100, board_thick])
            cube([55, 55, 4.5]); // Native Hex-BGA form factor
    }
}

module camm2_socket_clearance() {
    // Standard CAMM2-HX High-Speed memory module geometry layout
    color("DimGray") {
        cube([78, 64, 6.0]);
    }
}

module optoelectronic_card_clearance() {
    // Fiber Delay Loop Array chassis volume footprint
    color("RoyalBlue") {
        cube([110, 85, 22.0]);
    }
}

module satcom_pcie_card_clearance() {
    // Ka-Band Doppler tracking expansion card clearance profile
    color("Gold") {
        cube([140, 18, 450.0 / 10.0]); // Scaled card outline profile height
    }
}

module chassis_shell() {
    ext_w = motherboard_w + (chassis_wall * 2) + 10;
    ext_d = motherboard_d + (chassis_wall * 2) + 10;
    ext_h = interior_h + chassis_wall + board_thick;

    // Execute standard subtractive boolean geometry logic to create internal hollow area
    difference() {
        // Outer raw protective enclosure boundary
        color("SlateGray", 0.8) {
            translate([-chassis_wall - 5, -chassis_wall - 5, -chassis_wall])
                cube([ext_w, ext_d, ext_h]);
        }
        
        // Carve out main internal component housing cavity volume
        translate([-5, -5, 0])
            cube([motherboard_w + 10, motherboard_d + 10, interior_h + 10]);
            
        // Passive air exhaust grill openings cut out from the back panel wall boundary
        for(i = [0 : 25 : motherboard_w - 20]) {
            translate([i, motherboard_d + chassis_wall, interior_h / 2])
                rotate([90, 0, 0])
                    cylinder(h = chassis_wall + 15, r = 6.5, center = true);
        }
    }
}

// --- Composite Chassis Integration Composition Top Node ---
module assemble_chassis_workspace() {
    // 1. Position core surrounding shell framework
    chassis_shell();
    
    // 2. Position the main motherboard trace substrate model
    motherboard_base();
    
    // 3. Anchor DDR5-HX memory connectors to surface tracking configurations
    translate(camm2_offset)
        camm2_socket_clearance();
        
    // 4. Mount the Optoelectronic Array module safely into the bay coordinates
    translate(optical_offset)
        optoelectronic_card_clearance();
        
    // 5. Align the SatCom interface board into the PCIe slot pathing grid
    translate(satcom_offset)
        satcom_pcie_card_clearance();
}

// Instantiate final workspace visualization
assemble_chassis_workspace();
