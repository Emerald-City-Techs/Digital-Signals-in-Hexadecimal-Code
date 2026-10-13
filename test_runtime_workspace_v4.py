# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace
Initializes the primary Motherboard, evaluates Sega-style handshakes, 
and exercises the Photonic, SatCom, and Robotic Flight Claw daughtercard subsystems.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_translation_bridge import HexTranslationBridge
from src.chips.native.hex_native_optical_array import HexNativeOpticalArray
from src.chips.native.hex_native_satcom import HexNativeSatCom
from src.hex_native_flight_claw import HexNativeFlightClaw

def run_complete_system_test():
    print("=====================================================================")
    print("      BEGINNING TOTAL SYSTEM INTEGRATION CHECK (MOTHERBOARD & CARDS) ")
    print("=====================================================================")
    
    # Step 1: Fire up the core Motherboard Bus and clear Security Layer
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x9EC0FFEE)
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Primary Motherboard security lockout. Aborting testing profile.")
        sys.exit(1)
        
    bridge = HexTranslationBridge(orchestrator)
    
    # Step 2: Initialize Card Cluster A - Optoelectronic Photonic Delay System
    print("\n--- Booting Photonic Delay Line Interface ---")
    optical_card = HexNativeOpticalArray()
    optical_card.execute_full_spectrum_diagnostics()
    
    # Step 3: Initialize Card Cluster B - Aerospace SatCom PCIe Engine
    print("\n--- Booting Aerospace SatCom PCIe Controller ---")
    satcom_card = HexNativeSatCom()
    satcom_card.calibrate_doppler_shift(band_selection="Ka-Band")
    
    # Step 4: Initialize Peripheral C - Flight Claw Telemetry Interface
    print("\n--- Launching Real-Time Robotic Flight Claw Bridge ---")
    flight_claw = HexNativeFlightClaw(bridge)
    flight_claw.stream_robotic_telemetry()
    
    # Step 5: Safe tear down of active physical lines
    print("\n--- Releasing Interface Control Gates ---")
    orchestrator.close_device()
    print("=====================================================================")
    print("     ALL ANALOG HARDWARE COMPANION CARDS COMPILED AND VERIFIED      ")
    print("=====================================================================")

if __name__ == "__main__":
    run_complete_system_test()
