# File: src/chips/adapters/hex_display_bridge.py
"""
Revolutionary Technology (RT) Architecture - Hexadecimal Display Adapter Bridge
Translates internal 16-state analog voltage vector matrix tracks straight into
standard pixel video configurations (24-bit RGB or 8-bit monochromatic channels).
"""

class HexDisplayBridge:
    def __init__(self, target_width: int = 1920, target_height: int = 1080):
        """
        Initializes the video display bridge and establishes the pixel reference tables.
        """
        self.width = target_width
        self.height = target_height
        
        # 16 discrete physical voltage configurations (0.0000V up to 0.9375V)
        self.voltage_states = [round(i * 0.0625, 4) for i in range(16)]
        
        # Dynamic 16-state color rendering lookup map (maps a 4-bit nibble index to standard RGB color vectors)
        self.color_lookup_matrix = {
            0x0: (0, 0, 0),        # 0.0000V - Pitch Black / Blanking interval
            0x1: (32, 0, 64),      # 0.0625V - Deep Ultraviolet
            0x2: (0, 0, 128),      # 0.1250V - Pure Indigo Blue
            0x3: (0, 128, 255),    # 0.1875V - Cyan Stream
            0x4: (0, 255, 0),      # 0.2500V - Native Matrix Green
            0x5: (128, 255, 0),    # 0.3125V - Lime Phosphor
            0x6: (255, 255, 0),    # 0.3750V - Bright Yellow
            0x7: (255, 128, 0),    # 0.4375V - High-Intensity Orange
            0x8: (255, 0, 0),      # 0.5000V - Laser Warning Red
            0x9: (255, 0, 128),    # 0.5625V - Deep Magenta
            0xA: (128, 0, 255),    # 0.6250V - Electric Violet
            0xB: (200, 200, 255),  # 0.6875V - Glacial White-Blue
            0xC: (100, 100, 100),  # 0.7500V - Medium Slate Gray
            0xD: (180, 180, 180),  # 0.8125V - Bright Platinum Metallic
            0xE: (230, 240, 255),  # 0.8750V - Over-driven Soft White
            0xF: (255, 255, 255)   # 0.9375V - Absolute Saturation White
        }

    def _voltage_to_nibble(self, voltage: float) -> int:
        closest_v = min(self.voltage_references if hasattr(self, 'voltage_references') else self.voltage_states, 
                        key=lambda x: abs(x - round(voltage, 4)))
        return (self.voltage_references if hasattr(self, 'voltage_references') else self.voltage_states).index(closest_v)

    def convert_monochromatic_frame_vector(self, voltage_vector: list) -> list:
        """
        Translates a single raw voltage stream from an analog bus into an 8-bit monochromatic 
        grayscale pixel layout stream (0-255 luminance values).
        """
        print(f"[DisplayBridge] Generating monochromatic frame transformation layout for {len(voltage_vector)} nodes...")
        pixel_luminance_output = []
        
        for volt in voltage_vector:
            nibble = self._voltage_to_nibble(volt)
            # Scale 4-bit resolution (0-15) linearly into 8-bit color depth space (0-255)
            grayscale_byte = int((nibble / 15.0) * 255)
            pixel_luminance_output.append(grayscale_byte)
            
        return pixel_luminance_output

    def convert_parallel_chroma_rgb_vector(self, parallel_voltage_matrix: list) -> list:
        """
        Ingests three parallel 16-state analog tracks (representing Red, Green, and Blue 
        component channels) and maps them into 24-bit structural color pixel coordinates.
        
        Args:
            parallel_voltage_matrix (dict/list): Struct containing separate color element lists:
                                                {"R": [...], "G": [...], "B": [...]}
        """
        print("[DisplayBridge] Merging parallel analog tracks into true-color RGB pixel configurations...")
        r_track = parallel_voltage_matrix["R"]
        g_track = parallel_voltage_matrix["G"]
        b_track = parallel_voltage_matrix["B"]
        
        pixel_count = min(len(r_track), len(g_track), len(b_track))
        composite_rgb_pixels = []
        
        for idx in range(pixel_count):
            nibble_r = self._voltage_to_nibble(r_track[idx])
            nibble_g = self._voltage_to_nibble(g_track[idx])
            nibble_b = self._voltage_to_nibble(b_track[idx])
            
            # Reconstruct true 24-bit pixel components from the separate logic streams
            r_byte = int((nibble_r / 15.0) * 255)
            g_byte = int((nibble_g / 15.0) * 255)
            b_byte = int((nibble_b / 15.0) * 255)
            
            composite_rgb_pixels.append((r_byte, g_byte, b_byte))
            
        return composite_rgb_pixels

    def decode_voltage_via_lut(self, voltage_vector: list) -> list:
        """
        Routes analog signals straight through the hardware lookup table (LUT) matrix,
        yielding color coordinates directly for video controller frame processing.
        """
        video_output_pixels = []
        for volt in voltage_vector:
            nibble = self._voltage_to_nibble(volt)
            rgb_color = self.color_lookup_matrix.get(nibble, (0, 0, 0))
            video_output_pixels.append(rgb_color)
        return video_output_pixels
