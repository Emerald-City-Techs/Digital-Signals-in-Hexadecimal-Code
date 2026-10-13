# File: src/hex_thermal_monitor.py
"""
Revolutionary Technology (RT) Architecture - Physical Thermal Management Monitor
Regulates the RT-TOUGHAIR-16X Dual-Tower Blower array using native 16-state logic thresholds.
"""

class HexThermalMonitor:
    def __init__(self, hardware_orchestrator_instance):
        self.orchestrator = hardware_orchestrator_instance
        
        # 16-State Voltage Levels mapped to exact Fan Speed Targets
        self.voltage_states = [round(i * 0.0625, 4) for i in range(16)]
        
        # Thermal Limits (Degrees Celsius)
        self.temp_nominal = 35.0
        self.temp_warning = 65.0
        self.temp_critical = 85.0
        
        self.thermal_zones = {
            "ZONE_0_CORE_ALU": 32.5,
            "ZONE_1_DDR5_CAMM2": 34.0,
            "ZONE_2_PHOTONIC_LOOP": 28.0,
            "ZONE_3_TENSOR_CROSSBAR": 33.5
        }
        
        # RT-TOUGHAIR-16X Dual Fan Profiles
        self.active_voltage_rail_output = 0.0000
        self.dual_fans_rpm = 500
        self.system_throttled = False

    def evaluate_cooling_loop(self, injected_thermal_deltas: dict = None) -> str:
        if injected_thermal_deltas:
            for zone, temp in injected_thermal_deltas.items():
                if zone in self.thermal_zones:
                    self.thermal_zones[zone] = temp

        max_temp = max(self.thermal_zones.values())
        hottest_zone = max(self.thermal_zones, key=self.thermal_zones.get)
        
        # Map temperature range (30C to 90C) linearly into one of our 16 voltage index steps (0-15)
        clamped_temp = max(30.0, min(max_temp, 90.0))
        target_index = int(((clamped_temp - 30.0) / 60.0) * 15)
        
        # Set exact native analog voltage driving the dual-tower blowers
        self.active_voltage_rail_output = self.voltage_states[target_index]
        
        # Scale fan speeds based on our step profile (ranging up to 2500 RPM for high static pressure)
        self.dual_fans_rpm = 500 + (target_index * 133)
        
        print(f"\n[Thermal] Peak Temperature: {max_temp:.2f}°C in [{hottest_zone}]")
        print(f"[Thermal] RT-TOUGHAIR-16X Controller State: Modulating cooling line to {self.active_voltage_rail_output:.4f}V (State {hex(target_index).upper()})")
        print(f"[Thermal] Dual TOUGHFAN-16X Array running at: {self.dual_fans_rpm} RPM")

        if max_temp >= self.temp_critical:
            self.system_throttled = True
            return "CRITICAL_THROTTLING_ACTIVE"
        elif max_temp >= self.temp_warning:
            self.system_throttled = False
            return "WARNING_ELEVATED_COOLING"
        
        self.system_throttled = False
        return "NOMINAL_STABLE"
