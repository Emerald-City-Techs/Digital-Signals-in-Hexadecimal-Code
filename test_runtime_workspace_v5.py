# File: test_runtime_workspace.py
"""
Unified Hardware Runtime Verification Workspace - Extended Transmission Suite
Combines Motherboard Security, Daughtercard layers, and the User-Space Stream Tool.
"""

import os
import sys
from src.hardware_orchestrator import HardwareOrchestrator
from src.chips.adapters.hex_translation_bridge import HexTranslationBridge
from src.hex_stream_tool import HexStreamTool

def run_workspace_stream_test():
    print("=====================================================================")
    print("        LAUNCHING ACTIVE HIGH-SPEED USER-SPACE STREAM MODULE         ")
    print("=====================================================================")
    
    # 1. Initialize core system driver link and authentication engine
    orchestrator = HardwareOrchestrator()
    orchestrator.open_device()
    orchestrator.execute_sega_handshake(mock_challenge=0xDEED0B0A)
    
    if not orchestrator.authenticated:
        print("[CRITICAL] Locked architecture. Stream orchestration denied.")
        sys.exit(1)
        
    bridge = HexTranslationBridge(orchestrator)
    
    # 2. Bind the user-space streaming engine tool
    stream_tool = HexStreamTool(bridge)
    
    # 3. Create a temporary hardware file setup block to simulate file system metadata ingestion
    mock_file_path = "mock_system_payload.dat"
    with open(mock_file_path, "wb") as f:
        f.write(b"SystemData_Payload_Block_1_DDR5_HX_Calibration_Vector_Data_Stream_RT_Core_End_777")
        
    # 4. Stream data simultaneously across Slot 1 (DDR5 RAM), Slot 2 (Photonics), and Slot 3 (SatCom)
    target_hardware_slots = [1, 2, 3]
    print(f"[Workspace] Targets Armed: Slot Allocation Matrix -> {target_hardware_slots}")
    
    # Trigger active loop
    stream_success = stream_tool.stream_file_to_slots(
        file_path=mock_file_path, 
        target_slots=target_hardware_slots, 
        block_size_bytes=32
    )
    
    # 5. Cleanup runtime artifacts safely
    if os.path.exists(mock_file_path):
        os.remove(mock_file_path)
        
    orchestrator.close_device()

    if not stream_success:
        print("[FAIL] Streaming workspace loop testing failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_workspace_stream_test()
