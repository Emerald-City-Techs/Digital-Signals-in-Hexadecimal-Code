// ============================================================================
// RT Architecture: TUF GPU Chassis with Optoelectronic Isolation Chambers
// ============================================================================

$fn = 64;
variant = "monster"; 

module gpu_optical_chassis(type) {
    length = 320;
    height = 140;
    thickness = (type == "slim") ? 20 : ((type == "server") ? 40 : 60);
    
    // Scale loop chamber quantities based on structural profiles
    loop_chambers = (type == "monster") ? 8 : 4;

    difference() {
        // Main Heavy Armor Shell
        color([0.15, 0.15, 0.15]) 
            cube([length, thickness, height], center=true);
        
        // Main Core Airflow Channel
        translate([0, 0, height/4])
            cube([length - 60, thickness + 2, height/2], center=true);
            
        // Cut out light-tight physical memory loop isolation chambers
        for (i = [0 : loop_chambers - 1]) {
            translate([-length/4 + (i * 22), 0, -height/4]) {
                // Outer light shield enclosure cavity
                cube([16, thickness - 8, 25], center=true);
                
                // Sensor placement slot (Ocean Insight ST-VIS)
                translate([-4, 0, 0]) cylinder(h=25, r=4, center=true);
                
                // LED excitation alignment slot (Bridgelux Thrive 98)
                translate([4, 0, 0]) cylinder(h=25, r=3, center=true);
            }
        }
        
        // Dual M.2 SLI-Snap Bridge Slot Routing
        translate([length/2 - 30, 0, height/2 - 10])
            cube([42, thickness + 5, 12], center=true);
    }

    // Heavy Peg-Leg Support Stand for the 3-Slot Monster to avoid socket stress
    if (type == "monster") {
        color([0.3, 0.3, 0.3]) {
            translate([length/2 - 40, 0, -height/2 - 60]) cylinder(h=120, r=8, center=true);
            translate([length/2 - 40, 0, -height/2 - 120]) cylinder(h=10, r=25, center=true);
        }
    }
}

gpu_optical_chassis(variant);
