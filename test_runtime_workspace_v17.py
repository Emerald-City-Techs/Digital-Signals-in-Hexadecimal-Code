# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Display Bridge Suite
Processes multi-channel video frame buffers and validates RGB translation logic.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_display_bridge import HexDisplayBridge

def run_display_bridge_test():
    print("=====================================================================")
    print("       INITIALIZING HIGH-SPEED VIDEO FRAME BUFFER ADAPTER            ")
    print("=====================================================================")
    
    # 1. Engage low-level hardware interface locks
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x56494430) # "VID0" token
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect failure. Display bridge frame buffer unreachable.")
        sys.exit(1)
        
    # 2. Instantiate the Display Adapter Bridge module
    display_bridge = HexDisplayBridge(target_width=1920, target_height=1080)
    
    # 3. Test Profile A: Direct Hardware Look-Up Table Video Mapping
    print("\n--- Profile A: Testing Hardware LUT Color Rendering ---")
    mock_bus_video_signals = [0.0000, 0.2500, 0.5000, 0.9375] # States 0x0, 0x4, 0x8, 0xF
    print(f"Captured Core Bus Waveforms: {mock_bus_video_signals}")
    
    rendered_pixels = display_bridge.decode_voltage_via_lut(mock_bus_video_signals)
    print("Rendered RGB Pixel Output Profiles:")
    for idx, pixel in enumerate(rendered_pixels):
        print(f"  -> Signal Input Vector Slot [{idx}] -> Pixel Color Output: {pixel}")
        
    # 4. Test Profile B: Parallel Chroma-RGB Track Synthesis
    print("\n--- Profile B: Testing Parallel Chroma-RGB Track Convergence ---")
    # Simulate three separate data tracks outputting parallel component calculations
    mock_parallel_chroma_matrix = {
        "R": [0.5000, 0.0000, 0.9375], # Red track values
        "G": [0.0000, 0.2500, 0.9375], # Green track values
        "B": [0.1250, 0.0000, 0.0000]  # Blue track values
    }
    
    true_color_frame_buffer = display_bridge.convert_parallel_chroma_rgb_vector(mock_parallel_chroma_matrix)
    print(f"Synthesized True Color Frame Buffer Configuration (Pixels 0-2): {true_color_frame_buffer}")
    
    # 5. Clean teardown operations
    orchestrator.close_device()
    
    if rendered_pixels[1] == (0, 255, 0) and true_color_frame_buffer[0][0] == 255:
        print("\n[PASSED] Analog-to-Pixel matrix conversions and parallel component synthesis successful.")
    else:
        print("\n[FAILED] Display buffer quantization alignment fault detected.")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    run_display_bridge_test()
