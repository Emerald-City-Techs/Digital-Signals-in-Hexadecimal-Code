# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Power Delivery Suite
Monitors multi-rail telemetry, processes ammeter states, and validates overcurrent protection.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.hex_power_delivery import HexPowerDelivery

def run_power_delivery_test():
    print("=====================================================================")
    print("      INITIALIZING POWER DISTRIBUTION MANAGEMENT LAYER (PMIC)       ")
    print("=====================================================================")
    
    # 1. Open primary bus driver communication node
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x504D4943) # "PMIC" token
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect failure. PMIC telemetry bus unreachable.")
        sys.exit(1)
        
    # 2. Instantiate the Power Distribution Management object
    power_subsystem = HexPowerDelivery(orchestrator)
    
    # 3. Test Configuration A: Nominal running state loop
    print("\n--- Evaluation Scenario A: Verifying Baseline Operating Power ---")
    power_subsystem.poll_pmic_telemetry()
    status_a = power_subsystem.enforce_power_profile()
    print(f"PMIC Core State: {status_a} | Power Clamped Status: {power_subsystem.power_delivery_clamped}")
    
    # 4. Test Configuration B: Overcurrent spike handling (Circuit Protection Check)
    print("\n--- Evaluation Scenario B: Simulating Transient Load Surge Event ---")
    # Simulate a sudden massive load surge across the 3oz copper paths feeding the Tensor array
    malicious_load_spike = {
        "PLANE_CORE_ALU": {"voltage": 0.5000, "current_ma": 190.0},
        "PLANE_DDR5_CAMM2": {"voltage": 0.9375, "current_ma": 220.0},
        "PLANE_PHOTONIC_LOOP": {"voltage": 0.1250, "current_ma": 300.0},
        "PLANE_TENSOR_ARRAY": {"voltage": 0.8125, "current_ma": 520.0} # Breaches 450.0mA rail threshold
    }
    
    # Run data metrics through core enforcement filters to trigger mitigations
    status_b = power_subsystem.enforce_power_profile(custom_load_injection=malicious_load_spike)
    print(f"PMIC Core State: {status_b} | Power Clamped Status: {power_subsystem.power_delivery_clamped}")
    
    # 5. Clean teardown operations
    orchestrator.close_device()
    
    if power_subsystem.power_delivery_clamped and status_b == "EMERGENCY_CLAMP_ACTIVE":
        print("\n[PASSED] PMIC trace sensors and automated load limiting frameworks verified.")
    else:
        print("\n[FAILED] Circuit protection matrix failed to capture line overcurrent event.")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    run_power_delivery_test()
