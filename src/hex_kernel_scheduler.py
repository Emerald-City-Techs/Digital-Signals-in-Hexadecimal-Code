# File: src/hex_kernel_scheduler.py
"""
Revolutionary Technology (RT) Architecture - Hexadecimal Kernel Scheduler
Coordinates real-time task thread priority scheduling across 16 discrete analog
voltage execution slots while verifying strict memory isolation criteria via the MMU.
"""

import time
from collections import deque
from src.chips.native.hex_native_mmu import HexNativeMMU

class HexTask:
    def __init__(self, task_id: int, name: str, priority_nibble: int, target_virtual_addr: str, op_type: str = "READ"):
        """
        Represents a thread payload executing inside the Hexadecimal architecture framework.
        """
        self.task_id = task_id
        self.name = name
        self.priority = max(0, min(int(priority_nibble), 15)) # Restricted 0x0 to 0xF boundary
        self.target_virtual_addr = target_virtual_addr
        self.op_type = op_type
        
        # Drive task token voltage natively off its priority rank definition (0.0625V per interval step)
        self.assigned_voltage_token = round(self.priority * 0.0625, 4)

class HexKernelScheduler:
    def __init__(self, mmu_instance: HexNativeMMU):
        self.mmu = mmu_instance
        
        # 16 Separate execution priority scheduling channels (0 to 15)
        # 0x0 = Real-time core operations; 0xF = Lowest background housekeeping tasks
        self.scheduling_queues = {i: deque() for i in range(16)}
        self.execution_history = []

    def register_task(self, task: HexTask):
        """Places an inbound thread task into its corresponding priority voltage queue rail."""
        self.scheduling_queues[task.priority].append(task)
        print(f"[Scheduler] Registered Task #{task.task_id} [{task.name}] -> "
              f"Priority Queue: 0x{hex(task.priority)[2:].upper()} ({task.assigned_voltage_token:.4f}V)")

    def dispatch_next_task_slice(self) -> bool:
        """
        Scans priority channels from highest priority (0x0) to lowest (0xF)
        and executes the next ready thread after passing MMU checks.
        """
        for priority_level in range(16):
            if self.scheduling_queues[priority_level]:
                active_task = self.scheduling_queues[priority_level].popleft()
                print(f"\n[Scheduler] Dispatching Task #{active_task.task_id} [{active_task.name}] on Priority 0x{hex(priority_level)[2:].upper()}")
                
                # Enforce physical hardware memory isolation cross-checks via MMU layers
                try:
                    # Resolve physical target layout allocation boundaries using the task's voltage token
                    physical_frame = self.mmu.access_virtual_address(
                        virtual_hex_addr=active_task.target_virtual_addr,
                        requested_operation=active_task.op_type,
                        active_token_voltage=active_task.assigned_voltage_token
                    )
                    
                    # Simulation processing step
                    print(f"[Scheduler] [EXEC] Task '{active_task.name}' successfully processed slice data at Physical Frame {physical_frame}.")
                    self.execution_history.append((active_task.task_id, "SUCCESS"))
                    return True
                    
                except (PermissionError, MemoryError) as fault:
                    print(f"[Scheduler] [TRAP] Task '{active_task.name}' triggered a Hardware Protection Trap: {fault}")
                    print(f"            Terminating violating Task Thread ID #{active_task.task_id} immediately.")
                    self.execution_history.append((active_task.task_id, f"FAULT_ABORTED: {fault}"))
                    return True
                    
        return False # No processing payloads left inside system queues

    def execute_all_pending_tasks(self):
        """Runs the primary system thread resolution loop until all task lanes are clear."""
        print("\n[Scheduler] Beginning real-time operating system execution dispatcher loop...")
        while self.dispatch_next_task_slice():
            pass
        print("\n[Scheduler] All active real-time instruction streams resolved safely.")
