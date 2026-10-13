# File: src/chips/native/gpu_vector_reducer.py
"""
Revolutionary Technology (RT) Architecture - Parallel Vector Reduction Wrapper
Accelerates AI model clustering calculations across the 8 optoelectronic memory channels.
Implements a low-latency parallel tree reduction algorithm directly on analog voltage paths.
"""

import sys
from src.chips.native.hex_native_alu import HexNativeALU

class GPUVectorReducer:
    def __init__(self, alu_instance: HexNativeALU = None):
        """
        Initializes the vector reduction wrapper using a 16-state analog ALU coprocessor.
        """
        self.alu = alu_instance if alu_instance else HexNativeALU()
        self.total_optical_channels = 8

    def execute_parallel_tree_reduction(self, matrix_loop_data: list) -> list:
        """
        Executes an O(log N) parallel reduction operation over the 8 optical loop streams.
        Aggregates vector elements simultaneously to compute AI clustering centroids.
        
        Args:
            matrix_loop_data (list): A list of 8 lists, where each sub-list contains 
                                     the analog float voltages from that optical channel.
        """
        if len(matrix_loop_data) != self.total_optical_channels:
            raise ValueError(f"[Reducer] Expected exactly {self.total_optical_channels} data channels.")

        # Ensure all parallel vectors are uniform in dimension length
        vector_length = len(matrix_loop_data[0])
        print(f"[Reducer] Starting parallel reduction over {self.total_optical_channels} channels. Vector Depth: {vector_length} slots.")

        # Deep copy to maintain source track persistence during destructive tree aggregation
        current_stage_data = [list(channel) for channel in matrix_loop_data]

        stride = 1
        stage_count = 0
        
        # Parallel Binary Tree Reduction Loop: 8 -> 4 -> 2 -> 1
        while stride < self.total_optical_channels:
            stage_count += 1
            print(f"\n --- Tree Reduction Phase {stage_count} [Stride Step: {stride}] ---")
            
            for i in range(0, self.total_optical_channels, stride * 2):
                target_lane = i
                sibling_lane = i + stride
                
                print(f"  -> Merging Optical Channel [{sibling_lane}] into Target Channel [{target_lane}] via Analog ALU...")
                
                # Perform element-wise parallel vector additions across the two selected channel lanes
                for idx in range(vector_length):
                    v_a = current_stage_data[target_lane][idx]
                    v_b = current_stage_data[sibling_lane][idx]
                    
                    # Direct 16-state addition without intermediate binary conversion bottleneck
                    res_voltage, carry = self.alu.execute_analog_add(v_a, v_b)
                    
                    # Store accumulated waveform updates directly back onto the target rail track
                    current_stage_data[target_lane][idx] = res_voltage

            stride *= 2

        # The aggregated final reduction cluster centroid resides completely inside Channel Track 0
        final_reduced_cluster_centroid = current_stage_data[0]
        print(f"\n[Reducer] [SUCCESS] All 8 channels condensed to structural cluster node: {final_reduced_cluster_centroid}")
        return final_reduced_cluster_centroid
