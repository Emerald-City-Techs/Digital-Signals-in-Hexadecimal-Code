# File: src/hex_network_router.py
"""
Revolutionary Technology (RT) Architecture - Telemetry Network Router
Handles low-latency routing and network distribution of 16-state analog 
voltage vectors across connected multi-node hardware compute clusters.
"""

import sys
import json
import socket
import struct
from src.chips.native.hex_native_crypto import HexNativeCrypto

class HexNetworkRouter:
    def __init__(self, crypto_instance: HexNativeCrypto, host_ip: str = "127.0.0.1", port: int = 16570):
        """
        Initializes the telemetry router using an active crypto engine for secure verification.
        """
        self.crypto = crypto_instance
        self.host_ip = host_ip
        self.port = port
        self.socket = None
        self.cluster_nodes = {} # Maps node IDs to network addresses
        
        # Load the custom unique device hardware ID
        try:
            with open(self.crypto.key_storage_path, "r") as f:
                config = json.load(f)
            self.device_uuid = config.get("device_uuid", "RT-HEX-UNKNOWN")
        except Exception:
            self.device_uuid = "RT-HEX-DEFAULT"

    def register_cluster_node(self, node_id: int, ip_address: str, target_port: int):
        """Registers a remote cluster block destination node in the local routing table."""
        self.cluster_nodes[node_id] = {"ip": ip_address, "port": target_port}
        print(f"[NetRouter] Cluster Node registered: Node #{node_id} -> {ip_address}:{target_port}")

    def start_router_socket(self):
        """Initializes the network layer socket bound to the designated cluster interface."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.port))
        print(f"[NetRouter] Secure Telemetry socket listening on UDP interface {self.host_ip}:{self.port}")

    def broadcast_analog_frame(self, target_node_id: int, frame_id: int, encrypted_voltages: list) -> bool:
        """
        Packages 16-state encrypted analog float voltages into a secure UDP cluster datagram.
        
        Datagram Layout:
        [ 16-Byte UUID String ][ 4-Byte Frame ID ][ 2-Byte Element Count ][ N * 4-Byte Float Data elements ]
        """
        if target_node_id not in self.cluster_nodes:
            print(f"[NetRouter] [ERROR] Routing failed: Destination Node #{target_node_id} absent from routing map.")
            return False

        destination = self.cluster_nodes[target_node_id]
        element_count = len(encrypted_voltages)
        
        # 1. Pack fixed-size metadata boundaries
        # Pad UUID string to 16 bytes exactly to prevent network alignment buffer overruns
        uuid_bytes = self.device_uuid.encode('utf-8')[:16].ljust(16, b'\x00')
        header_bytes = struct.pack(">16sIH", uuid_bytes, frame_id, element_count)
        
        # 2. Pack the raw float values of the 16-state voltage array elements
        payload_bytes = bytearray(header_bytes)
        for volt in encrypted_voltages:
            payload_bytes.extend(struct.pack(">f", volt))
            
        # 3. Secure dispatch over the network plane
        try:
            if self.socket:
                self.socket.sendto(payload_bytes, (destination["ip"], destination["port"]))
                print(f"[NetRouter] Secure Broadcast complete: Sent Frame #{frame_id} ({element_count} analog states) "
                      f"to Node #{target_node_id} [{destination['ip']}:{destination['port']}]")
                return True
        except Exception as e:
            print(f"[NetRouter] [ABORT] Network delivery failed over hardware bus: {e}")
            return False
        return False

    def shutdown_router(self):
        """Closes the socket link cleanly."""
        if self.socket:
            self.socket.close()
            print("[NetRouter] Router interface unlinked safely.")
