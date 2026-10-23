// File: hardware/chassis_assembly.scad
/**
 * Revolutionary Technology (RT) Architecture - Chassis Assembly Blueprint
 * Integrates the RT-TOUGHAIR-16X CPU Cooler and Media Jack Mounting Brackets.
 * All dimensions specified in millimeters (mm).
 */

$fn = 64; // High render circular detail resolution

// --- Core Mechanical Dimensions ---
motherboard_w  = 305;  // Standard industrial format footprint width
motherboard_d  = 244;  // Standard depth clearance
board_thick    = 2.4;  // Rigid 8-layer high-density PCB depth
chassis_wall   = 4.0;  // Reinforced structural frame wall thickness
interior_h     = 195;  // Vertical height clearance for dual-tower cooler

// --- Footprint Spatial Offsets ---
camm2_offset   = [45,  160, board_thick];
optical_offset = [160, 40,  board_thick];
satcom_offset  = [20,  40,  board_thick];
cpu_offset     = [110, 100, board_thick];

// --- Media Jack Bracket Spatial Offsets (Rear I/O Panel) ---
display_jack_offset = [260, motherboard_d - 12, board_thick];
audio_jack_offset   = [210, motherboard_d - 12, board_thick];

module motherboard_base() {
    color("DarkGreen") {
        cube([motherboard_w, motherboard_d, board_thick]);
    }
    // CPU Component Positioning Block
    color("LightGray") {
        translate([cpu_offset[0], cpu_offset[1], cpu_offset[2]])
            cube([55, 55, 4.5]);
    }
}

module rt_toughair_16x_clearance() {
    // Custom Dual-Tower Heatsink Assembly inspired by Thermaltake TOUGHAIR 710
    translate([cpu_offset[0] - 46, cpu_offset[1] - 45, cpu_offset[2] + 4.5]) {
        color("Silver", 0.7) cube([148.5, 45, 160]); // Tower 1
        color("DimGray", 0.8) translate([0, 49, 0]) cube([140, 25, 140]); // Mid Fan
        color("Silver", 0.7) translate([0, 78, 0]) cube([148.5, 45, 160]); // Tower 2
        color("DimGray", 0.8) translate([4.25, -28, 23]) cube([140, 25, 140]); // Outer Fan
    }
}

module display_jack_bracket() {
    // Structural parameters for the RT-DisplayBridge HDMI-HX Port
    color("LightSlateGray") {
        // Main Port Enclosure Body
        cube([25, 12, 15]);
        // Reinforced Grounding Flange Plate Mounts
        translate([-4, -2, 0]) cube([33, 2, 17]);
    }
}

module audio_jack_bracket() {
    // Structural parameters for the RT-AudioJack 4-Channel HX Port
    color("DarkSlateGray") {
        // Main Port Enclosure Body
        cube([30, 12, 12]);
        // Physical Divider Bracket to isolate trace induction fields
        translate([-3, -2, 0]) cube([36, 2, 14]);
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
        // Outer raw protective enclosure boundary
        color("SlateGray", 0.3) {
            translate([-chassis_wall - 5, -chassis_wall - 5, -chassis_wall])
                cube([ext_w, ext_d, ext_h]);
        }
        
        // Carve out main internal component housing cavity volume
        translate([-5, -5, 0])
            cube([motherboard_w + 10, motherboard_d + 10, interior_h + 10]);
            
        // Cut out Display Bridge Connector Port through the rear wall array
        translate([display_jack_offset[0], motherboard_d, display_jack_offset[2]])
            cube([25, chassis_wall + 10, 15]);
            
        // Cut out Audio Codec Connector Port through the rear wall array
        translate([audio_jack_offset[0], motherboard_d, audio_jack_offset[2]])
            cube([30, chassis_wall + 10, 12]);
            
        // Cooling air exhaust grill openings 
        for(i = [0 : 25 : motherboard_w - 60]) {
            translate([i, motherboard_d + chassis_wall, interior_h / 2])
                rotate([90, 0, 0])
                    cylinder(h = chassis_wall + 15, r = 6.5, center = true);
        }
    }
}

module assemble_chassis_workspace() {
    chassis_shell();
    motherboard_base();
    rt_toughair_16x_clearance();
    
    // Position media brackets onto rear-panel coordinates
    translate(display_jack_offset) display_jack_bracket();
    translate(audio_jack_offset) audio_jack_bracket();
    
    translate(camm2_offset) camm2_socket_clearance();
    translate(optical_offset) optoelectronic_card_clearance();
    translate(satcom_offset) satcom_pcie_card_clearance();
}

assemble_chassis_workspace();
