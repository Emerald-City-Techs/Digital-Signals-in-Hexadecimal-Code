# File: src/chips/adapters/hex_audio_codec.py
"""
Revolutionary Technology (RT) Architecture - Hexadecimal Audio Codec Adapter
Translates internal 16-state analog voltage vector arrays into standard multi-channel
audio frequency waves, mapping discrete logic levels directly to spatial acoustic tracks.
"""

import math

class HexAudioCodec:
    def __init__(self, sample_rate_hz: int = 48000):
        """
        Initializes the multi-channel sound card codec bridge.
        """
        self.sample_rate = sample_rate_hz
        self.voltage_states = [round(i * 0.0625, 4) for i in range(16)]
        
        # Define native multi-channel audio path alignments
        self.channel_map = {
            0: "FRONT_LEFT",
            1: "FRONT_RIGHT",
            2: "CENTER_DIALOG",
            3: "LOW_FREQUENCY_EFFECTS_SUB"
        }

    def _voltage_to_nibble(self, voltage: float) -> int:
        closest_v = min(self.voltage_states, key=lambda x: abs(x - round(voltage, 4)))
        return self.voltage_states.index(closest_v)

    def decode_stream_to_stereo_waves(self, hex_voltage_stream: list) -> dict:
        """
        Demultiplexes a single high-speed internal voltage stream into separate 
        Left and Right acoustic tracks, mapping 16-state values to balanced analog amplitudes.
        """
        print(f"[AudioCodec] Splitting {len(hex_voltage_stream)} bus nodes into physical stereo fields...")
        stereo_buffer = {"LEFT": [], "RIGHT": []}
        
        for idx, volt in enumerate(hex_voltage_stream):
            nibble = self._voltage_to_nibble(volt)
            
            # Translate 4-bit space (0-15) directly into linear normalized amplitude scale (-1.0 to 1.0)
            normalized_amplitude = ((nibble / 15.0) * 2.0) - 1.0
            
            # Distribute tracking arrays alternatively across physical speaker pins
            if idx % 2 == 0:
                stereo_buffer["LEFT"].append(round(normalized_amplitude, 4))
            else:
                stereo_buffer["RIGHT"].append(round(normalized_amplitude, 4))
                
        return stereo_buffer

    def modulate_quadraphonic_surround_space(self, raw_data_blocks: list) -> dict:
        """
        Spatially routes 16-state computing outputs simultaneously across 4 hardware channels
        without standard signal compression delay chains.
        """
        print("[AudioCodec] Matrixing native hexadecimal arrays to 4-channel surround vectors...")
        surround_matrix = {ch_name: [] for ch_name in self.channel_map.values()}
        
        for idx, volt in enumerate(raw_data_blocks):
            nibble = self._voltage_to_nibble(volt)
            normalized_amplitude = ((nibble / 15.0) * 2.0) - 1.0
            
            # Map index states to the corresponding hardware channel boundary
            target_channel = self.channel_map[idx % 4]
            surround_matrix[target_channel].append(round(normalized_amplitude, 4))
            
        return surround_matrix
