# File: src/chips/native/hex_native_alu.py
"""
Revolutionary Technology (RT) Architecture - Native Hexadecimal Analog ALU
Performs direct 16-state analog arithmetic operations on voltage level inputs.
Includes carry/borrow overflows and voltage saturation clamping diagnostics.
"""

class HexNativeALU:
    def __init__(self, step_increment: float = 0.0625):
        # 16 discrete physical voltage configurations (0.0000V to 0.9375V)
        self.voltage_references = [round(i * step_increment, 4) for i in range(16)]
        self.saturation_max_v = 1.0000  # Hard ceiling for hardware amplifier protection
        self.ground_min_v = 0.0000

    def _voltage_to_nibble(self, voltage: float) -> int:
        """Helper to resolve an analog voltage reading to its closest logical 4-bit nibble value."""
        target_v = round(voltage, 4)
        closest_v = min(self.voltage_references, key=lambda x: abs(x - target_v))
        return self.voltage_references.index(closest_v)

    def _nibble_to_voltage(self, nibble: int) -> float:
        """Helper to map a logical 4-bit integer to its exact analog reference rail value."""
        clamped_nibble = max(0, min(int(nibble), 15))
        return self.voltage_references[clamped_nibble]

    def execute_analog_add(self, voltage_a: float, voltage_b: float) -> tuple:
        """
        Performs non-linear 16-state analog addition.
        Combines two voltage waves, returns the resulting output voltage and a carry nibble flag.
        """
        nibble_a = self._voltage_to_nibble(voltage_a)
        nibble_b = self._voltage_to_nibble(voltage_b)
        
        raw_sum = nibble_a + nibble_b
        carry = 1 if raw_sum > 15 else 0
        result_nibble = raw_sum % 16
        
        # Check if the combined physical waves trigger hardware voltage rail clipping
        actual_combined_voltage = voltage_a + voltage_b
        clipped = actual_combined_voltage >= self.saturation_max_v
        
        result_voltage = self._nibble_to_voltage(result_nibble)
        
        print(f"[HexALU] ADD: 0x{hex(nibble_a)[2:].upper()} + 0x{hex(nibble_b)[2:].upper()} "
              f"-> Result: 0x{hex(result_nibble)[2:].upper()} (Carry: {carry}) "
              f"| Rails: {result_voltage:.4f}V [Physical Wave Combined: {actual_combined_voltage:.4f}V | Clipped: {clipped}]")
              
        return result_voltage, carry

    def execute_analog_subtract(self, voltage_a: float, voltage_b: float) -> tuple:
        """
        Performs 16-state analog subtraction.
        Calculates difference between two voltage signals, returning resulting voltage and a borrow flag.
        """
        nibble_a = self._voltage_to_nibble(voltage_a)
        nibble_b = self._voltage_to_nibble(voltage_b)
        
        raw_diff = nibble_a - nibble_b
        borrow = 1 if raw_diff < 0 else 0
        result_nibble = raw_diff % 16
        
        # Verify physical potential drop doesn't dive beneath structural ground limits
        actual_dropped_voltage = voltage_a - voltage_b
        ground_clamped = actual_dropped_voltage < self.ground_min_v
        
        result_voltage = self._nibble_to_voltage(result_nibble)
        
        print(f"[HexALU] SUB: 0x{hex(nibble_a)[2:].upper()} - 0x{hex(nibble_b)[2:].upper()} "
              f"-> Result: 0x{hex(result_nibble)[2:].upper()} (Borrow: {borrow}) "
              f"| Rails: {result_voltage:.4f}V [Physical Wave Dropped: {actual_dropped_voltage:.4f}V | Ground Clamped: {ground_clamped}]")
              
        return result_voltage, borrow

    def execute_analog_bitwise_xor(self, voltage_a: float, voltage_b: float) -> float:
        """
        Performs a logical XOR cross-match by evaluating logic levels on parallel operational rails.
        Useful for running fast physical decryption streams.
        """
        nibble_a = self._voltage_to_nibble(voltage_a)
        nibble_b = self._voltage_to_nibble(voltage_b)
        
        result_nibble = nibble_a ^ nibble_b
        result_voltage = self._nibble_to_voltage(result_nibble)
        
        print(f"[HexALU] XOR: 0x{hex(nibble_a)[2:].upper()} ^ 0x{hex(nibble_b)[2:].upper()} "
              f"-> Result: 0x{hex(result_nibble)[2:].upper()} | Output: {result_voltage:.4f}V")
              
        return result_voltage
