# File: test_runtime_workspace.py
"""
Runtime Workspace Verification Wrapper - File System Mapping Expansion
Validates byte data flow from raw files to physical scrambled analog configurations.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_translation_bridge import HexTranslationBridge

def run_workspace_test():
    print("=====================================================================")
    print("     TESTING FILE SYSTEM CONVERSION VIA HEX TRANSLATION BRIDGE        ")
    print("=====================================================================")
    
    # 1. Set up low-level orchestrator interface layer
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    
    # 2. Unlocking security framework
    orchestrator.execute_sega_handshake(mock_challenge=0x53454741) # "SEGA" challenge
    
    # 3. Bind the transformation bridge module
    bridge = HexTranslationBridge(orchestrator)
    
    # 4. Simulate reading an original standard file system structural header (e.g., FAT / EXT signature)
    mock_file_system_header = b"FAT32   " # Standard 8-byte file system type signature
    print(f"\n[Input Data Source] Original Raw File System Header: {mock_file_system_header}")
    
    # 5. Step Forward: Compress 8-bit structure to 16-state obfuscated voltage paths
    scrambled_bus_voltages = bridge.encode_file_system_block(mock_file_system_header)
    print("\n[Bridge Encode] Generated Physical Scrambled Voltage Signatures (First 6 slots shown):")
    print(f"  -> {scrambled_bus_voltages[:6]}")
    
    # 6. Step Reverse: Reconstruct real binary data off of intercepted board vectors
    restored_binary_data = bridge.decode_file_system_block(scrambled_bus_voltages)
    print(f"\n[Bridge Decode] Reconstruction Output: {restored_binary_data}")
    
    if restored_binary_data == mock_file_system_header:
        print("\n[PASSED] Round-trip file system structure conversion verified.")
    else:
        print("\n[FAILED] Verification mismatch during hardware-software synchronization.")
        sys.exit(1)

    orchestrator.close_device()
    print("=====================================================================")

if __name__ == "__main__":
    run_workspace_test()
