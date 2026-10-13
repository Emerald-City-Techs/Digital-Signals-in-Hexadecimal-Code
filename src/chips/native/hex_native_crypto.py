# File: src/chips/native/hex_native_crypto.py
"""
Revolutionary Technology (RT) Architecture - Native Hexadecimal Cryptographic Accelerator
Implements an onboarding identity generator to prevent duplicate default keys,
and performs 16-state hardware-accelerated block ciphers for scheduled kernels.
"""

import os
import secrets
import json

class HexNativeCrypto:
    def __init__(self, key_storage_path: str = "hardware/secure_identity.json"):
        self.key_storage_path = key_storage_path
        self.voltage_states = [round(i * 0.0625, 4) for i in range(16)]
        
        # Runtime master keys mapped to 4-bit hexadecimal blocks
        self.master_hardware_key = []
        self.session_cipher_matrix = {}
        
        # Trigger identity allocation on module instantiation
        self._ensure_unique_hardware_identity()

    def _ensure_unique_hardware_identity(self):
        """
        Enforces unique device fingerprints. If no profile exists, uses cryptographically 
        secure entropy to generate a custom 32-nibble default hardware key matrix.
        """
        if os.path.exists(self.key_storage_path):
            try:
                with open(self.key_storage_path, "r") as f:
                    config = json.load(f)
                self.master_hardware_key = [int(x, 16) for x in config["master_key_hex"]]
                print(f"[HexCrypto] Secure Hardware Identity loaded from disk. Device ID: {config['device_uuid']}")
                return
            except Exception as e:
                print(f"[HexCrypto] [WARN] Identity configuration corrupt: {e}. Regenerating...")

        # Identity Generator Execution Loop (First-Time Initialization)
        print("[HexCrypto] [INITIALIZATION] Generating unique Master Key block to eliminate default signature risks...")
        
        # Generate 128 bits of high-entropy randomness split into 32 logical 4-bit nibbles
        unique_bytes = secrets.token_bytes(16)
        generated_key = []
        for byte in unique_bytes:
            generated_key.extend([(byte >> 4) & 0x0F, byte & 0x0F])
            
        device_uuid = secrets.token_hex(8).upper()
        self.master_hardware_key = generated_key
        
        # Persist profile to disk storage path
        os.makedirs(os.path.dirname(self.key_storage_path), exist_ok=True)
        config_payload = {
            "device_uuid": f"RT-HEX-{device_uuid}",
            "master_key_hex": [hex(n)[2:].upper() for n in generated_key]
        }
        
        with open(self.key_storage_path, "w") as f:
            json.dump(config_payload, f, indent=4)
            
        print(f"[HexCrypto] [SUCCESS] New hardware fingerprint created and locked to storage target. UUID: RT-HEX-{device_uuid}")

    def compute_session_cipher_matrix(self, sega_challenge_token: int):
        """
        Derives an active session transposition table by blending the physical 
        Sega challenge token with the unique hardware master key layer.
        """
        print(f"[HexCrypto] Scrambling active cipher matrix matching Sega Token: 0x{sega_challenge_token:08X}")
        
        # Mix entropy across the active channels
        for idx in range(16):
            mix_factor = (sega_challenge_token >> (idx * 2)) & 0x0F
            shuffled_index = (self.master_hardware_key[idx % len(self.master_hardware_key)] + mix_factor) % 16
            self.session_cipher_matrix[idx] = shuffled_index

    def encrypt_analog_bus_vector(self, clear_voltages: list) -> list:
        """
        Accelerates pipeline block encryption. Direct hardware routing maps 
        clear voltage lines to dynamic obfuscated physical states.
        """
        if not self.session_cipher_matrix:
            raise RuntimeError("[HexCrypto] Encryption rejected: Session cipher matrix uninitialized.")
            
        encrypted_voltages = []
        for voltage in clear_voltages:
            # Map physical voltage back to its discrete index slot
            logical_idx = max(0, min(int(round(voltage / 0.0625)), 15))
            
            # Route through the hardware-shuffled transposition matrix
            encrypted_idx = self.session_cipher_matrix.get(logical_idx, 0)
            encrypted_voltages.append(self.voltage_states[encrypted_idx])
            
        return encrypted_voltages
