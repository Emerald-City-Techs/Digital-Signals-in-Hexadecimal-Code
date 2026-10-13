# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Audio Codec Suite
Processes raw bus logic profiles into normalized multi-channel surround sound configurations.
"""

import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_audio_codec import HexAudioCodec

def run_audio_codec_test():
    print("=====================================================================")
    print("        INITIALIZING MULTI-CHANNEL HARDWARE AUDIO CODEC             ")
    print("=====================================================================")
    
    # 1. Open primary bus driver link and pass Sega authentication
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0x534F554E) # "SOUN" token
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Interconnect failure. Sound codec system unreachable.")
        sys.exit(1)
        
    # 2. Instantiate the Audio Codec module
    audio_codec = HexAudioCodec(sample_rate_hz=48000)
    
    # 3. Test Profile A: Stereo Demultiplexing Sequence
    print("\n--- Profile A: Demultiplexing High-Speed Bus Stream to Stereo ---")
    mock_audio_bus_signals = [0.0000, 0.9375, 0.2500, 0.5000, 0.0625, 0.8125] # States 0x0, 0xF, 0x4, 0x8, 0x1, 0xD
    print(f"Captured System Audio Voltages: {mock_audio_bus_signals}")
    
    stereo_waves = audio_codec.decode_stream_to_stereo_waves(mock_audio_bus_signals)
    print("Generated Audio Amplitude Tracks:")
    print(f"  -> Physical LEFT  Speaker Rail Amplitudes: {stereo_waves['LEFT']}")
    print(f"  -> Physical RIGHT Speaker Rail Amplitudes: {stereo_waves['RIGHT']}")
    
    # 4. Test Profile B: Quadraphonic Surround Space Mapping
    print("\n--- Profile B: Routing Vectors to Quadraphonic Spatial Rails ---")
    # Simulate a deep computing telemetry packet passing to audio diagnostic outputs
    mock_telemetry_waveforms = [0.1250, 0.0625, 0.8750, 0.9375, 0.2500, 0.5625, 0.3125, 0.0000]
    
    surround_sound_fields = audio_codec.modulate_quadraphonic_surround_space(mock_telemetry_waveforms)
    print("Decoupled Surround Sound Channel Matrix Mapping:")
    for ch_name, waveforms in surround_sound_fields.items():
        print(f"  -> {ch_name}: {waveforms}")
        
    # 5. Clean teardown operations
    orchestrator.close_device()
    
    # Simple semantic evaluation checks for successful structural tracking
    if len(stereo_waves["LEFT"]) == 3 and "CENTER_DIALOG" in surround_sound_fields:
        print("\n[PASSED] Analog logic vector to audio wave frequency matrix processing complete.")
    else:
        print("\n[FAILED] Audio track distribution vector boundary mismatch.")
        sys.exit(1)
    print("=====================================================================")

if __name__ == "__main__":
    run_audio_codec_test()
