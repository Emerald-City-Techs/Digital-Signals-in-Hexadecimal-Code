# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Thermal Suite
Monitors trace heat profiles, simulates data workloads, and tests active cooling controllers.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.hex_thermal_monitor import HexThermalMonitor

def run_thermal_monitor_test():
    print("=====================================================================")
    print("      INITIALIZING PHYSICAL THERMAL INFRASTRUCTURE MONITORING SUITE  ")
    print("=====================================================================")
    
    # 1. Open communications with host system bus driver layer
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x5448524D) # "THRM" token
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect failure. Thermal monitoring bus unreachable.")
        sys.exit(1)
        
    # 2. Spin up the primary Physical Thermal Management Monitor component
    thermal_unit = HexThermalMonitor(orchestrator)
    
    # 3. Scenario A: Evaluate baseline cooling state
    print("\n--- Evaluation Scenario A: Evaluating Baseline Idle Thermal State ---")
    thermal_unit.poll_hardware_sensors()
    status_a = thermal_unit.evaluate_cooling_loop()
    print(f"Subsystem Status: {status_a} | Active Fan Speed: {thermal_unit.exhaust_blower_rpm} RPM")
    
    # 4. Scenario B: Simulate high-density AI tensor workload heat generation
    print("\n--- Evaluation Scenario B: Simulating High-Throughput Matrix Workload ---")
    # Simulate a sudden heat spike inside the thick copper paths of the Tensor Crossbar Array
    workload_heat_spikes = {
        "ZONE_0_CORE_ALU": 42.0,
        "ZONE_1_DDR5_CAMM2": 51.5,
        "ZONE_2_PHOTONIC_LOOP": 31.0,
        "ZONE_3_TENSOR_CROSSBAR": 88.5  # Exceeds the 85.0°C critical threshold
    }
    
    # Pass heat measurements through control loops to evaluate response
    status_b = thermal_unit.evaluate_cooling_loop(injected_thermal_deltas=workload_heat_spikes)
    print(f"Subsystem Status: {status_b} | Active Fan Speed: {thermal_unit.exhaust_blower_rpm} RPM")
    print(f"Emergency Throttling Tripped Flag: {thermal_unit.system_throttled}")
    
    # 5. Safe system shutdown
    orchestrator.close_device()
    
    if thermal_unit.system_throttled and thermal_unit.exhaust_blower_rpm == 6500:
        print("\n[PASSED] Thermal monitoring arrays and active cooling controllers verified successfully.")
    else:
        print("\n[FAILED] Active loop failed to mitigate critical temperature excursion event.")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    run_thermal_monitor_test()
