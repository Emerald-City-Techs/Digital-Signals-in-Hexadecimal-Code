# File: src/hex_stream_tool.py
"""
Revolutionary Technology (RT) Architecture - User-Space Data Streaming Tool
Orchestrates high-speed 16-state packet parsing and multi-slot distribution loops.
"""

import sys
import time
import struct
from src.chips.adapters.hex_translation_bridge import HexTranslationBridge

class HexStreamTool:
    def __init__(self, translation_bridge_instance, memory_subsystem_instance = None):
        """
        Initializes the streaming tool with an active translation bridge context.
        """
        self.bridge = translation_bridge_instance
        self.memory_subsystem = memory_subsystem_instance
        self.active_stream = False
        self.packet_counter = 0

    def craft_hex_packet(self, slot_id: int, command_code: int, data_payload: bytes) -> dict:
        """
        Encapsulates raw data into a structured 16-state architecture frame packet.
        
        Packet Format:
        [ 2-byte Magic Header ][ 1-byte Slot ID ][ 1-byte Command ][ 4-byte Length ][ Variable Scrambled Data Payload ]
        """
        self.packet_counter += 1
        payload_len = len(data_payload)
        
        # Craft a structural binary header block
        header_bytes = struct.pack(">HBBTI", 0x4858, slot_id, command_code, self.packet_counter, payload_len)
        
        # Compile complete physical packet structure using translation bridge matrices
        raw_binary_packet = header_bytes + data_payload
        scrambled_analog_voltages = self.bridge.encode_file_system_block(raw_binary_packet)
        
        return {
            "packet_id": self.packet_counter,
            "target_slot": slot_id,
            "command": command_code,
            "voltage_stream": scrambled_analog_voltages,
            "raw_length_bytes": len(raw_binary_packet)
        }

    def stream_file_to_slots(self, file_path: str, target_slots: list, block_size_bytes: int = 64):
        """
        Pipes a target file configuration stream directly across the physical board expansion slots.
        """
        if not self.bridge.orchestrator.authenticated:
            print("[StreamTool] [CRITICAL] Rejection: Logic bus is locked. Cannot open stream.")
            return False

        if not os.path.exists(file_path):
            print(f"[StreamTool] Error: Target payload source file not found: {file_path}")
            return False

        print(f"[StreamTool] Initiating active transmission pipeline for source: {file_path}")
        self.active_stream = True
        total_bytes_pushed = 0
        start_time = time.time()

        try:
            with open(file_path, "rb") as f:
                while self.active_stream:
                    chunk = f.read(block_size_bytes)
                    if not chunk:
                        break # End of data stream target
                    
                    # Round-robin target slot distribution sequencing
                    for slot in target_slots:
                        # Command Code 0xA3 represents an active streaming write step configuration
                        packet = self.craft_hex_packet(slot_id=slot, command_code=0xA3, data_payload=chunk)
                        
                        # Route down to physical hardware channels
                        self._dispatch_to_bus(packet)
                        total_bytes_pushed += len(chunk)
                        
            duration = time.time() - start_time
            print("\n=====================================================================")
            print(f"[StreamTool] [SUCCESS] Transmission complete. Total Bytes Streamed: {total_bytes_pushed}")
            print(f"[StreamTool] Outbound execution time: {duration:.4f}s | Packets Sent: {self.packet_counter}")
            print("=====================================================================")
            return True
        except Exception as e:
            print(f"[StreamTool] [ABORT] Critical pipeline routing fault: {e}")
            return False
        finally:
            self.active_stream = False

    def _dispatch_to_bus(self, formatted_packet: dict):
        """Dispatches the processed 16-state analog packet directly to hardware slots."""
        slot_map = {
            1: "CONN_DDR5_CAMM2 [Memory Subsystem]",
            2: "CONN_PHOTONIC_LOOP [Optoelectronic Delay Array]",
            3: "CONN_SATCOM_PCIE [Doppler Tracking Card]"
        }
        
        target_name = slot_map.get(formatted_packet["target_slot"], "Unknown Expansion Slot")
        print(f"  -> [Bus Dispatch] Packet #{formatted_packet['packet_id']} -> Routing to {target_name}")
        print(f"     [Signals] Outbound Track Length: {formatted_packet['raw_length_bytes']} Bytes | First 4 Volts: {formatted_packet['voltage_stream'][:4]}")
