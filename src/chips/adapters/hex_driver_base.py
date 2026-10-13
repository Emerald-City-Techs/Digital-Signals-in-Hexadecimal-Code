class HexBaseDriver:
    """Base driver for mapping native binary software calls into 16-state physical traces."""
    def __init__(self, trace_id, voltage_min=0.0, voltage_max=1.0):
        self.trace_id = trace_id
        self.step_size = 0.0625

    def value_to_voltage(self, hex_char: str) -> float:
        """Converts a standard hexadecimal nibble (0-F) to its target analog voltage."""
        val = int(hex_char, 16)
        return round(val * self.step_size, 4)

    def voltage_to_value(self, voltage: float) -> str:
        """Quantizes an analog voltage sample back to a hex token."""
        index = min(max(int(round(voltage / self.step_size)), 0), 15)
        return hex(index)[2:].upper()

# Example subclass for custom video matrix
class HexDisplayDriver(HexBaseDriver):
    def transmit_frame_buffer(self, hex_string_data: str):
        voltage_stream = [self.value_to_voltage(char) for char in hex_string_data]
        # Pipe directly into your multisim/hardware injection interface
        return voltage_stream
