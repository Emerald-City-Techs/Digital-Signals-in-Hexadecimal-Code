# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Cryptographic Accelerator Suite
Initializes system identities, generates custom key environments, and executes block ciphers.
"""

import os
import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.native.hex_native_crypto import HexNativeCrypto

def run_crypto_integration_test():
    print("=====================================================================")
    print("       INITIALIZING COPROCESSOR HARDWARE CRYPTOGRAPHIC CORE          ")
    print("=====================================================================")
    
    # Target file paths
    secure_id_path = "hardware/secure_identity.json"
    
    # 1. Clear out stale testing states to showcase first-launch generation mechanics
    if os.path.exists(secure_id_path):
        os.remove(secure_id_path)

    # 2. Fire up low-level interface links
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x43525950) # "CRYP" challenge
    
    # 3. Instantiate the Cryptographic Module (Triggers Identity Generator loop)
    crypto_engine = HexNativeCrypto(key_storage_path=secure_id_path)
    
    # 4. Synchronize with the Sega Security handshake layer to deploy active ciphers
    crypto_engine.compute_session_cipher_matrix(sega_challenge_token=0x43525950)
    
    # 5. Simulate processing a live data payload traveling down an active kernel track
    clear_system_voltages = [0.0000, 0.2500, 0.5625, 0.1250] # 0x0, 0x4, 0x9, 0x2
    print(f"\n[Data Inbound] Original Operational Clear Bus Waveforms: {clear_system_voltages}")
    
    # Execute direct 16-state hardware block transformation
    scrambled_bus_outputs = crypto_engine.encrypt_analog_bus_vector(clear_system_voltages)
    print(f"[Crypto Out] Hard-Accelerated Obfuscated Voltages Result : {scrambled_bus_outputs}")
    
    # 6. Verify profile configuration file was generated cleanly on disk
    if os.path.exists(secure_id_path):
        print("\n[PASSED] Cryptographic isolation workspace initialized with a unique identity.")
    else:
        print("\n[FAILED] Identity configuration file failed to write to destination.")
        sys.exit(1)

    orchestrator.close_device()
    print("=====================================================================")

if __name__ == "__main__":
    run_crypto_integration_test()
