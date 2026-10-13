// ============================================================================
// RT Architecture: Over-Engineered TUF Hexadecimal GPU Structural Chassis
// ============================================================================

$fn = 64;

// Module selector: "slim", "server", or "monster"
variant = "monster"; 

module gpu_core_chassis(type) {
    // Structural Base Dimensions
    length = 320;
    height = 140;
    
    // Set thickness factor based on card slots (1 slot = 20mm, 2 = 40mm, 3 = 60mm)
    thickness = (type == "slim") ? 20 : ((type == "server") ? 40 : 60);
    
    echo("Synthesizing Layout for Variant Target: ", type, "Thickness: ", thickness, "mm");

    difference() {
        // Main TUF Aluminum Armor Enclosure Block
        color([0.15, 0.15, 0.15]) 
            cube([length, thickness, height], center=true);
        
        // Extrude Outflow Channels for Heavy Thermal Vapor Shrouds
        translate([0, 0, height/4])
            cube([length - 40, thickness + 2, height/2], center=true);
            
        // Cutout for the Embedded M.2 SLI-Snap Interconnect Bridge
        translate([length/2 - 30, 0, height/2 - 10])
            cube([42, thickness + 5, 12], center=true);
    }
    
    // Model the Thick 3oz High-Current Board Input Leads
    color([0.85, 0.65, 0.15]) { // Gold/Copper tracking
        translate([-length/2 + 20, -thickness/2 - 2, -height/2 + 5])
            cube([60, 4, 8]);
        translate([-length/2 + 100, -thickness/2 - 2, -height/2 + 5])
            cube([60, 4, 8]);
    }
    
    // Model the Addressable LED-illuminated Hexadecimal CAMM2 Memory Blocks
    color([0.2, 0.8, 1.0]) { // LED Cyan glow lines
        translate([-40, -thickness/2 - 1, 10]) cube([80, 2, 25]);
        translate([-40, thickness/2 - 1, 10]) cube([80, 2, 25]);
    }

    // Conditional Component: Add the Heavy Peg-Leg Support Stand for the 3-Slot Monster
    if (type == "monster") {
        color([0.3, 0.3, 0.3]) {
            // Drop bracket connection arm down to desk surface boundary
            translate([length/2 - 40, 0, -height/2 - 60])
                cylinder(h=120, r=8, center=true);
            // Solid base foot pad
            translate([length/2 - 40, 0, -height/2 - 120])
                cylinder(h=10, r=25, center=true);
        }
        echo("[STRUCTURAL WARNING] Peg-Leg deployment required to prevent PCIe socket shear.");
    }
}

// Instantiate target block
gpu_core_chassis(variant);
