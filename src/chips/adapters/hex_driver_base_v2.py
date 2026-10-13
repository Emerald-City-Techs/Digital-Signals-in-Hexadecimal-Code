# File: src/chips/adapters/hex_driver_base.py
import abc

class HexDriverBase(abc.ABC):
    def __init__(self):
        self.device_node = "/dev/hex_compute"
        self.authenticated = False

    @abc.abstractmethod
    def read_voltage_bus(self) -> list:
        """Reads current real-time voltage patterns from device blocks."""
        pass

    @abc.abstractmethod
    def inject_signal_stream(self, binary_payload: bytes) -> bool:
        """Translates and injects raw streams into 16-state registers."""
        pass
