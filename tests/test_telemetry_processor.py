"""
Unit Tests — Drone Telemetry Processor
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 1.0 | Date: May 8, 2026

Testing approach: Black-box testing — tests verify input/output behavior
without relying on internal implementation details of the processor.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from drone.telemetry_processor import TelemetryProcessor, TelemetryData, OptimizedPath


class TestTelemetryProcessing:
    """Black-box tests for telemetry data processing."""

    def setup_method(self):
        self.proc = TelemetryProcessor("DRONE-TEST-01")

    def test_process_valid_telemetry(self):
        """Valid raw data should produce structured TelemetryData."""
        raw = {
            'lat': 39.7392, 'lon': -104.9903, 'alt': 50.0,
            'battery': 85.0, 'rssi_5g': -75.0, 'rssi_sat': -90.0,
            'sensors': {'nir': 0.8, 'red': 0.2}
        }
        result = self.proc.process_telemetry(raw)
        assert isinstance(result, TelemetryData)
        assert result.drone_id == "DRONE-TEST-01"
        assert result.latitude == 39.7392
        assert result.altitude == 50.0
        print(f"PASS: Valid telemetry processed — lat={result.latitude}")

    def test_connectivity_mode_5g(self):
        """Strong 5G signal should select 5G mode."""
        raw = {'rssi_5g': -75.0, 'rssi_sat': -90.0}
        result = self.proc.process_telemetry(raw)
        assert result.connectivity_mode == '5G'
        print(f"PASS: 5G mode selected — RSSI=-75dBm")

    def test_connectivity_mode_satellite(self):
        """Weak 5G but good satellite should select SATELLITE."""
        raw = {'rssi_5g': -95.0, 'rssi_sat': -85.0}
        result = self.proc.process_telemetry(raw)
        assert result.connectivity_mode == 'SATELLITE'
        print(f"PASS: Satellite mode selected — 5G weak, SAT strong")

    def test_connectivity_mode_offline(self):
        """Both signals weak should select OFFLINE."""
        raw = {'rssi_5g': -95.0, 'rssi_sat': -105.0}
        result = self.proc.process_telemetry(raw)
        assert result.connectivity_mode == 'OFFLINE'
        print(f"PASS: Offline mode — both signals below threshold")

    def test_missing_fields_defaults(self):
        """Missing fields should use defaults without crashing."""
        raw = {}
        result = self.proc.process_telemetry(raw)
        assert result.latitude == 0.0
        assert result.battery_level == 100.0
        assert result.connectivity_mode == 'OFFLINE'
        print("PASS: Missing fields handled with defaults")

    def test_buffer_accumulation(self):
        """Telemetry buffer should accumulate readings."""
        for i in range(5):
            self.proc.process_telemetry({'lat': 39.0 + i * 0.001})
        summary = self.proc.get_buffer_summary()
        assert summary['total_readings'] == 5
        print(f"PASS: Buffer accumulated {summary['total_readings']} readings")

    def test_buffer_summary_empty(self):
        """Empty buffer should return empty dict."""
        summary = self.proc.get_buffer_summary()
        assert summary == {}
        print("PASS: Empty buffer returns empty dict")


class TestHaversineDistance:
    """Black-box tests for GPS distance calculation."""

    def setup_method(self):
        self.proc = TelemetryProcessor("DRONE-TEST-01")

    def test_same_point_zero_distance(self):
        """Same coordinates should give zero distance."""
        dist = self.proc.haversine_distance(39.7392, -104.9903, 39.7392, -104.9903)
        assert dist == pytest.approx(0.0, abs=0.001)
        print("PASS: Same point = 0 km distance")

    def test_known_distance(self):
        """Denver to Boulder (~40km) should be approximately correct."""
        dist = self.proc.haversine_distance(39.7392, -104.9903, 40.0150, -105.2705)
        assert 35 < dist < 45  # Approximately 40km
        print(f"PASS: Denver-Boulder distance = {dist:.1f} km (expected ~40km)")

    def test_symmetry(self):
        """Distance A->B should equal distance B->A."""
        dist_ab = self.proc.haversine_distance(39.7, -104.9, 40.0, -105.2)
        dist_ba = self.proc.haversine_distance(40.0, -105.2, 39.7, -104.9)
        assert dist_ab == pytest.approx(dist_ba, abs=0.001)
        print(f"PASS: Symmetric distance — A->B = B->A = {dist_ab:.3f} km")

    def test_short_distance(self):
        """Very close points should give small distance."""
        dist = self.proc.haversine_distance(39.7392, -104.9903, 39.7395, -104.9900)
        assert dist < 0.1  # Less than 100 meters
        print(f"PASS: Short distance = {dist*1000:.1f} meters")


class TestPathOptimization:
    """Black-box tests for GPS flight path optimization."""

    def setup_method(self):
        self.proc = TelemetryProcessor("DRONE-TEST-01")

    def test_empty_waypoints(self):
        """Empty waypoint list should return zero-distance path."""
        result = self.proc.optimize_flight_path([])
        assert result.total_distance_km == 0.0
        assert result.waypoints == []
        print("PASS: Empty waypoints handled")

    def test_single_waypoint(self):
        """Single waypoint should return zero distance."""
        result = self.proc.optimize_flight_path([(39.7, -104.9)])
        assert result.total_distance_km == 0.0
        print("PASS: Single waypoint = 0 distance")

    def test_optimization_reduces_distance(self):
        """Optimized path should be <= original sequential distance."""
        # Create waypoints that are clearly suboptimal in sequential order
        waypoints = [
            (39.70, -104.90),  # Start
            (39.80, -104.80),  # Far away
            (39.71, -104.91),  # Back near start
            (39.81, -104.81),  # Far again
            (39.72, -104.92),  # Back near start again
        ]
        result = self.proc.optimize_flight_path(waypoints)
        assert result.total_distance_km <= result.original_distance_km
        print(f"PASS: Optimized={result.total_distance_km:.3f}km <= Original={result.original_distance_km:.3f}km")

    def test_energy_savings_calculated(self):
        """Energy savings percentage should be non-negative."""
        waypoints = [
            (39.70, -104.90),
            (39.80, -104.80),
            (39.71, -104.91),
            (39.81, -104.81),
        ]
        result = self.proc.optimize_flight_path(waypoints)
        assert result.energy_savings_pct >= 0.0
        print(f"PASS: Energy savings = {result.energy_savings_pct}%")

    def test_flight_time_estimated(self):
        """Flight time should be positive for multi-waypoint paths."""
        waypoints = [
            (39.70, -104.90),
            (39.75, -104.85),
            (39.80, -104.80),
        ]
        result = self.proc.optimize_flight_path(waypoints)
        assert result.estimated_flight_time_min > 0
        print(f"PASS: Estimated flight time = {result.estimated_flight_time_min} min")

    def test_all_waypoints_visited(self):
        """All waypoints should appear in the optimized path."""
        waypoints = [
            (39.70, -104.90),
            (39.75, -104.85),
            (39.80, -104.80),
        ]
        result = self.proc.optimize_flight_path(waypoints)
        assert len(result.waypoints) == len(waypoints)
        for wp in waypoints:
            assert wp in result.waypoints
        print(f"PASS: All {len(waypoints)} waypoints visited in optimized path")

    def test_custom_start_point(self):
        """Custom start point should be first in optimized path."""
        waypoints = [(39.70, -104.90), (39.75, -104.85), (39.80, -104.80)]
        start = (39.80, -104.80)
        result = self.proc.optimize_flight_path(waypoints, start_point=start)
        assert result.waypoints[0] == start
        print(f"PASS: Custom start point respected — first={result.waypoints[0]}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
