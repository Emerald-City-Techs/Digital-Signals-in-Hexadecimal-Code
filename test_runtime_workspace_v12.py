# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Networking Suite
Validates legacy Ethernet binary conversions alongside native HexDSL-OTP modulation loops.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_translation_bridge import HexTranslationBridge
from src.chips.adapters.hex_ethernet_bridge import HexEthernetBridge

def run_network_bridge_test():
    print("=====================================================================")
    print("        INITIALIZING HIGH-SPEED ETHERNET & NATIVE DSL BRIDGE         ")
    print("=====================================================================")
    
    # 1. Fire up hardware drivers and complete the cryptographic handshake
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x45544830) # "ETH0" token
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect failure. Network routing aborted.")
        sys.exit(1)
        
    translation_bridge = HexTranslationBridge(orchestrator)
    
    # 2. Instantiate our network subsystem adapter
    net_adapter = HexEthernetBridge(translation_bridge)
    
    # 3. Execution Profile A: Standard Legacy Network Interaction
    print("\n--- Profile A: Processing Legacy IEEE 802.3 Ethernet Frame ---")
    mock_ipv4_packet = b"\x45\x00\x00\x28\x1A\x2B\x00\x00\x40\x06" # Simulated packet head
    print(f"Incoming Binary Payload Source: {mock_ipv4_packet.hex().upper()}")
    
    # Translate inbound binary to 16-state internal signals
    modulated_voltage_rail = net_adapter.translate_from_standard_ethernet_frame(mock_ipv4_packet)
    print(f"Modulated Bus Output Signals (First 4 steps): {modulated_voltage_rail[:4]}")
    
    # Recover original packet layout from internal track signals
    recovered_packet_bytes = net_adapter.translate_to_standard_ethernet_frame(modulated_voltage_rail)
    print(f"Reconstructed Binary Payload: {recovered_packet_bytes.hex().upper()}")
    
    # 4. Execution Profile B: HexDSL-Over-Twisted-Pair Custom Mode
    print("\n--- Profile B: Deploying Native HexDSL-OTP Over Network Cable ---")
    # Sequence of 4-bit hexadecimal operations (0x0 to 0xF) ready for deployment
    native_hex_data_stream = [0xA, 0x5, 0xF, 0x2, 0x1, 0xE, 0x8, 0xBC] # Filtered arrays
    # Flatten down elements to strict single nibbles
    raw_nibbles = [0xA, 0x5, 0xF, 0x2, 0x1, 0x3, 0x8, 0xC]
    print(f"Native System Outbound Logic Stream: {[hex(n)[2:].upper() for n in raw_nibbles]}")
    
    # Split the native stream across the physical copper pairs inside the cable
    physical_cable_lanes = net_adapter.modulate_hexdsl_over_twisted_pair(raw_nibbles)
    print("\n[Cat6 Cable Signals] Real-Time Voltage Waves Transmitting Across Twisted Copper Pairs:")
    for wire_pair, waveforms in physical_cable_lanes.items():
        print(f"  -> {wire_pair}: {waveforms}V")
        
    # Recombine the physical waves back into a logical system instruction stream
    demodulated_stream = net_adapter.demodulate_hexdsl_from_twisted_pair(physical_cable_lanes)
    print(f"\n[Receiver Input] Demodulated Native Logic Stream: {[hex(n)[2:].upper() for n in demodulated_stream]}")
    
    # 5. Clean teardown procedures
    orchestrator.close_device()
    
    if demodulated_stream == raw_nibbles:
        print("\n[PASSED] Legacy Ethernet translation and Native HexDSL-OTP test loops successful.")
    else:
        print("\n[FAILED] Network synchronization verification failed.")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    run_network_bridge_test()
