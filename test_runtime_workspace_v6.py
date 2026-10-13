# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - ALU Expansion
Processes dynamic streamed signal waves directly through the native analog math core.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_translation_bridge import HexTranslationBridge
from src.chips.native.hex_native_alu import HexNativeALU

def run_alu_integration_test():
    print("=====================================================================")
    print("        INITIALIZING COPROCESSOR ANALOG ARITHMETIC UNIT (ALU)        ")
    print("=====================================================================")
    
    # 1. Boot Motherboard bus and pass Sega-style verification step
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0xABADC0DE)
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect Lockout. ALU bus lines unrouted.")
        sys.exit(1)
        
    bridge = HexTranslationBridge(orchestrator)
    
    # 2. Instantiate the Analog Calculation Core
    alu = HexNativeALU()
    
    # 3. Simulate two parallel incoming streams of physical data (e.g., streaming file bytes)
    # Target Values: 0x4 (0.2500V) and 0xD (0.8125V)
    stream_voltage_1 = 0.2500  
    stream_voltage_2 = 0.8125  
    
    print(f"\n[Signals] Intercepting Waveform A: {stream_voltage_1:.4f}V")
    print(f"[Signals] Intercepting Waveform B: {stream_voltage_2:.4f}V\n")
    
    # 4. Trigger Hardware Arithmetic Blocks
    print("--- Running Direct Arithmetic Sequences ---")
    # Addition Test (0x4 + 0xD = 0x11 -> 0x1 with Carry 1)
    res_add_v, carry_flag = alu.execute_analog_add(stream_voltage_1, stream_voltage_2)
    
    # Subtraction Test (0x4 - 0xD = -0x9 -> 0x7 with Borrow 1)
    res_sub_v, borrow_flag = alu.execute_analog_subtract(stream_voltage_1, stream_voltage_2)
    
    # Bitwise Encryption/Decryption Test (0x4 ^ 0xD = 0x9 -> 0.5625V)
    res_xor_v = alu.execute_analog_bitwise_xor(stream_voltage_1, stream_voltage_2)
    
    print("\n--- Verification Cycle Complete ---")
    orchestrator.close_device()
    print("=====================================================================")
    print("         HEXADECIMAL NATIVE MATH COPROCESSOR STACK IS ONLINE         ")
    print("=====================================================================")

if __name__ == "__main__":
    run_alu_integration_test()
