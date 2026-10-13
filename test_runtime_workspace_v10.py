# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Telemetry Network Router Suite
Initializes the system identity, encrypts states, and broadcasts analog arrays to cluster nodes.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.native.hex_native_crypto import HexNativeCrypto
from src.hex_network_router import HexNetworkRouter

def run_network_integration_test():
    print("=====================================================================")
    print("       INITIALIZING SECURE TELEMETRY NETWORK CLUSTER ROUTER          ")
    print("=====================================================================")
    
    # 1. Secure physical system driver interface linkage
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x4E455452) # "NETR" token
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect failure. Network routing aborted.")
        sys.exit(1)
        
    # 2. Fire up the Cryptographic and Identity Module
    crypto_engine = HexNativeCrypto()
    crypto_engine.compute_session_cipher_matrix(sega_challenge_token=0x4E455452)
    
    # 3. Instantiate and configure the Telemetry Network Router
    router = HexNetworkRouter(crypto_instance=crypto_engine)
    router.start_router_socket()
    
    # Map a remote cluster computation destination target node (e.g., node 5)
    router.register_cluster_node(node_id=5, ip_address="127.0.0.1", target_port=16575)
    
    # 4. Generate data, apply 16-state hardware encryption, and broadcast the payload
    clear_operational_voltages = [0.0625, 0.5000, 0.9375, 0.2500] # 0x1, 0x8, 0xF, 0x4
    print(f"\n[Core Payload] Input Clear Voltage Rails: {clear_operational_voltages}")
    
    encrypted_signal_vector = crypto_engine.encrypt_analog_bus_vector(clear_operational_voltages)
    print(f"[Crypto Pack] Hardware-Scrambled Vector Targets: {encrypted_signal_vector}\n")
    
    # Send the packet array down the wire to target cluster block node #5
    broadcast_success = router.broadcast_analog_frame(
        target_node_id=5, 
        frame_id=4004, 
        encrypted_voltages=encrypted_signal_vector
    )
    
    # 5. Clean teardown procedures
    router.shutdown_router()
    orchestrator.close_device()
    
    if broadcast_success:
        print("\n[PASSED] Telemetry frame packaged and broadcast across the matrix cleanly.")
    else:
        print("\n[FAILED] Network allocation buffer dispatch failure.")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    run_network_integration_test()
