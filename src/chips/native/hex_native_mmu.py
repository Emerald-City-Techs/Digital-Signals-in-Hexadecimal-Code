# File: src/chips/native/hex_native_mmu.py
"""
Revolutionary Technology (RT) Architecture - Native Hexadecimal Memory Management Unit
Handles virtual-to-physical address translation, page protection attributes,
and analog memory isolation faults across the DDR5-HX / CAMM2 memory space.
"""

class HexNativeMMU:
    def __init__(self, ddr5_ram_instance=None):
        self.ram = ddr5_ram_instance
        # Map 16 discrete 4-bit voltage keys to strict structural hardware domain permissions
        self.protection_matrix = {
            0x0: "KERNEL_SECURE_RWX", # 0.0000V - Core Firmware Space Only
            0x1: "KERNEL_READ_ONLY",   # 0.0625V - Driver System Code
            0x2: "SYSTEM_BUS_IO",      # 0.1250V - PCIe / MMIO Allocation Linkage
            0x3: "OPTICAL_DELAY_BUFF", # 0.1875V - Photonic Memory Cache Area
            0x4: "USER_SPACE_RW",      # 0.2500V - Standard App Application Space
            0x5: "USER_SPACE_RO",      # 0.3125V - Protected Application Shared Data
            0x6: "OBFUSCATED_TEMP_RAM",# 0.3750V - Sega-Scrambled Volatile Data Bank
            # 0x7 to 0xF reserved for high-performance telemetry / SatCom execution buffers
        }
        
        # Virtual Page Table mapping directory: Virtual Hex Address String -> (Physical Frame Int, Protection Token Int)
        self.page_table_directory = {}

    def map_virtual_page(self, virtual_hex_addr: str, physical_frame: int, protection_token: int):
        """
        Registers a 16-state memory layout translation sequence inside the hardware directory.
        
        Args:
            virtual_hex_addr (str): Crux string matching hex bounds (e.g., "0x7F2A")
            physical_frame (int): The destination physical hardware index offset inside RAM channels
            protection_token (int): Hex nibble (0-15) defining domain rules
        """
        token_nibble = protection_token & 0x0F
        clean_addr = virtual_hex_addr.upper().replace("0X", "")
        
        self.page_table_directory[clean_addr] = {
            "physical_frame": physical_frame,
            "protection_token": token_nibble,
            "domain_rule": self.protection_matrix.get(token_nibble, "RESERVED_RESTRICTED")
        }
        print(f"[HexMMU] Page Link Registered: Virtual 0x{clean_addr} -> Physical Frame {physical_frame} "
              f"| Token: 0x{hex(token_nibble)[2:].upper()} ({self.page_table_directory[clean_addr]['domain_rule']})")

    def access_virtual_address(self, virtual_hex_addr: str, requested_operation: str, active_token_voltage: float) -> int:
        """
        Validates access rights using the physical voltage token and maps virtual addresses to hardware layouts.
        
        Args:
            virtual_hex_addr (str): Target address string.
            requested_operation (str): "READ", "WRITE", or "EXECUTE".
            active_token_voltage (float): The actual analog voltage value representing the caller's privilege level.
        """
        clean_addr = virtual_hex_addr.upper().replace("0X", "")
        
        # 1. Look up address in the virtual directory table
        if clean_addr not in self.page_table_directory:
            print(f"[HexMMU] [HARDWARE FAULT] Page Missing Fault: 0x{clean_addr} not allocated in current context.")
            raise MemoryError("PAGE_MISSING_FAULT")
            
        page_entry = self.page_table_directory[clean_addr]
        
        # 2. Convert caller's physical voltage token back to its 4-bit logical integer representation
        resolved_caller_token = max(0, min(int(round(active_token_voltage / 0.0625)), 15))
        required_protection_token = page_entry["protection_token"]
        
        print(f"[HexMMU] Translation Attempt: 0x{clean_addr} | Caller Token: 0x{hex(resolved_caller_token)[2:].upper()} "
              f"({active_token_voltage:.4f}V) | Target Constraint: 0x{hex(required_protection_token)[2:].upper()}")

        # 3. Enforce Domain Boundary Isolation Protection Rules
        # Kernel rules (0x0, 0x1) require an exact privilege level match to prevent host cross-talk or user privilege escalation
        if required_protection_token in [0x0, 0x1] and resolved_caller_token != required_protection_token:
            print(f"[HexMMU] [SECURITY VIOLATION] Analog Memory Protection Fault! Caller privilege is insufficient.")
            raise PermissionError("ANALOG_MEMORY_PROTECTION_FAULT")
            
        # User space validation checks (Read-Only restrictions)
        if page_entry["domain_rule"] == "USER_SPACE_RO" and requested_operation == "WRITE":
            print(f"[HexMMU] [SECURITY VIOLATION] Write Fault! Attempted memory modification on a Read-Only domain.")
            raise PermissionError("WRITE_PROTECTION_FAULT")

        # 4. Successful translation handoff
        print(f"[HexMMU] [PASS] Access Granted. Address verified to physical offset frame: {page_entry['physical_frame']}")
        return page_entry["physical_frame"]
