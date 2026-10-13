# File: src/hex_power_delivery.py
"""
Revolutionary Technology (RT) Architecture - Power Distribution Management Layer
Regulates current draw limits (mA) across the 16 analog logic voltage rails.
Protects 2oz/3oz physical copper traces from transient power sags and rail oscillations.
"""

import time

class HexPowerDelivery:
    def __init__(self, hardware_orchestrator_instance):
        """
        Initializes the PMIC layer mapped to the active hardware orchestration substrate.
        """
        self.orchestrator = hardware_orchestrator_instance
        
        # 16 Discrete Reference Voltage Rails Matching System Increments
        self.voltage_references = [round(i * 0.0625, 4) for i in range(16)]
        
        # System Hardware Power Limits (Milliamp thresholds per power plane)
        self.max_current_per_rail_ma = 450.0  # Max limit per individual voltage signal trace
        self.max_aggregate_system_ma = 4500.0 # Emergency shutdown limit across motherboard
        
        # Operational Real-Time Current Tracking State Map (mA)
        self.power_plane_telemetry = {
            "PLANE_CORE_ALU": {"voltage": 0.5000, "current_ma": 180.0},
            "PLANE_DDR5_CAMM2": {"voltage": 0.9375, "current_ma": 240.0},
            "PLANE_PHOTONIC_LOOP": {"voltage": 0.1250, "current_ma": 310.0},
            "PLANE_TENSOR_ARRAY": {"voltage": 0.8125, "current_ma": 190.0}
        }
        
        self.pmic_status = "POWER_RAILS_STABLE"
        self.power_delivery_clamped = False

    def poll_pmic_telemetry(self) -> dict:
        """
        Simulates standard hardware bus polling of on-board shunt resistor ammeters.
        Returns live running current draw profiles across primary load networks.
        """
        if not self.orchestrator.authenticated:
            print("[PMIC] [WARN] Interconnect bus locked. Returning low-current standby baseline.")
            return {plane: {"voltage": 0.0, "current_ma": 5.0} for plane in self.power_plane_telemetry}
            
        return self.power_plane_telemetry

    def enforce_power_profile(self, custom_load_injection: dict = None) -> str:
        """
        Active hardware feedback enforcement loop. Scans target planes for amperage
        spikes, handles multi-rail power balancing, and prevents line-impedance drops.
        """
        if custom_load_injection:
            # Inject dynamic load factors to test boundary condition safety nets
            for plane, stats in custom_load_injection.items():
                if plane in self.power_plane_telemetry:
                    self.power_plane_telemetry[plane] = stats

        total_system_draw_ma = 0.0
        overcurrent_detected = False
        offending_plane = None

        print("[PMIC] Analyzing voltage rail telemetry and load balancing factors...")

        for plane_name, metrics in self.power_plane_telemetry.items():
            volts = metrics["voltage"]
            curr_ma = metrics["current_ma"]
            total_system_draw_ma += curr_ma
            
            # 1. Enforce protection check against maximum load limits for an individual trace path
            if curr_ma > self.max_current_per_rail_ma:
                overcurrent_detected = True
                offending_plane = plane_name
                print(f"[PMIC] [ALERT] Overcurrent threshold breached on {plane_name}: {curr_ma:.2f}mA drawn!")

        # Calculate live aggregate metrics
        print(f"[PMIC] Total System Draw: {total_system_draw_ma:.2f}mA / {self.max_aggregate_system_ma}mA")

        # 2. Evaluate state engine decisions based on physical load limits
        if total_system_draw_ma >= self.max_aggregate_system_ma or overcurrent_detected:
            self.pmic_status = "EMERGENCY_CLAMP_ACTIVE"
            self.power_delivery_clamped = True
            print(f"[PMIC] [CRITICAL PROTECTION FAULT] Triggering current clamp on load tracks.")
            print(f"       -> Hard clamping operational power steps down to ground (0.0000V).")
            
            # Mitigate the spike by driving the load values low
            for plane_name in self.power_plane_telemetry:
                self.power_plane_telemetry[plane_name]["current_ma"] = 10.0
                self.power_plane_telemetry[plane_name]["voltage"] = 0.0000
        else:
            self.pmic_status = "POWER_RAILS_STABLE"
            self.power_delivery_clamped = False
            print("[PMIC] All power domains running inside safe operating limits.")

        return self.pmic_status
