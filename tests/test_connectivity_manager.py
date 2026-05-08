"""
Unit Tests — Hybrid Connectivity Manager
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 1.0 | Date: May 8, 2026

Testing approach: White-box testing — tests verify internal RSSI thresholds,
failover logic, timing advance calculations, and Doppler shift compensation.
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from connectivity.hybrid_connectivity_manager import (
    HybridConnectivityManager, ConnectivityMode, ConnectivityStatus
)


class TestConnectivitySwitching:
    """White-box tests for connectivity mode selection logic."""

    def setup_method(self):
        self.mgr = HybridConnectivityManager()

    def test_5g_preferred_when_strong(self):
        """5G should be selected when RSSI > -90 dBm."""
        status = self.mgr.evaluate_and_switch(rssi_5g=-75.0, rssi_ntn=-85.0)
        assert status.mode == ConnectivityMode.FIVE_G
        assert status.is_urllc is True
        assert status.latency_ms < 10.0
        print(f"PASS: 5G selected — RSSI=-75dBm, Latency={status.latency_ms}ms")

    def test_satellite_fallback(self):
        """Satellite NTN should activate when 5G RSSI <= -90 dBm."""
        status = self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-85.0)
        assert status.mode == ConnectivityMode.SATELLITE_NTN
        assert status.is_urllc is False
        assert status.latency_ms < 50.0
        print(f"PASS: Satellite fallback — RSSI_5G=-95dBm, Latency={status.latency_ms}ms")

    def test_offline_mode(self):
        """Offline when both signals below threshold."""
        status = self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-105.0)
        assert status.mode == ConnectivityMode.OFFLINE
        assert status.bandwidth_mbps == 0.0
        print("PASS: Offline mode — both signals below threshold")

    def test_5g_boundary_threshold(self):
        """RSSI exactly at -90 dBm should NOT select 5G (must be > -90)."""
        status = self.mgr.evaluate_and_switch(rssi_5g=-90.0, rssi_ntn=-85.0)
        assert status.mode == ConnectivityMode.SATELLITE_NTN
        print("PASS: Boundary test — RSSI=-90dBm triggers satellite fallback")

    def test_none_rssi_5g(self):
        """None 5G RSSI should fall through to satellite."""
        status = self.mgr.evaluate_and_switch(rssi_5g=None, rssi_ntn=-85.0)
        assert status.mode == ConnectivityMode.SATELLITE_NTN
        print("PASS: None 5G RSSI falls through to satellite")

    def test_both_none(self):
        """Both None should result in offline."""
        status = self.mgr.evaluate_and_switch(rssi_5g=None, rssi_ntn=None)
        assert status.mode == ConnectivityMode.OFFLINE
        print("PASS: Both None = offline")

    def test_failover_counter(self):
        """Failover count should increment on each satellite switch."""
        self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-85.0)
        self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-85.0)
        stats = self.mgr.get_failover_stats()
        assert stats['total_failovers'] == 2
        print(f"PASS: Failover counter = {stats['total_failovers']}")

    def test_5g_bandwidth(self):
        """5G mode should report 1000 Mbps bandwidth."""
        status = self.mgr.evaluate_and_switch(rssi_5g=-70.0, rssi_ntn=-85.0)
        assert status.bandwidth_mbps == 1000.0
        print(f"PASS: 5G bandwidth = {status.bandwidth_mbps} Mbps")

    def test_satellite_bandwidth(self):
        """Satellite mode should report 100 Mbps bandwidth."""
        status = self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-85.0)
        assert status.bandwidth_mbps == 100.0
        print(f"PASS: Satellite bandwidth = {status.bandwidth_mbps} Mbps")


class TestTimingAdvance:
    """White-box tests for NTN timing advance calculation."""

    def setup_method(self):
        self.mgr = HybridConnectivityManager()

    def test_high_elevation_low_ta(self):
        """High elevation (90°) should produce minimum timing advance."""
        ta = self.mgr.calculate_timing_advance(90.0)
        assert ta > 0
        assert ta < 5000  # Should be relatively low at zenith
        print(f"PASS: TA at 90° elevation = {ta:.2f} µs")

    def test_low_elevation_high_ta(self):
        """Low elevation (10°) should produce higher timing advance."""
        ta_low = self.mgr.calculate_timing_advance(10.0)
        ta_high = self.mgr.calculate_timing_advance(90.0)
        assert ta_low > ta_high
        print(f"PASS: TA at 10° ({ta_low:.0f}µs) > TA at 90° ({ta_high:.0f}µs)")

    def test_ta_within_3gpp_limit(self):
        """Timing advance should never exceed 3GPP maximum (45000 µs)."""
        ta = self.mgr.calculate_timing_advance(10.0)
        assert ta <= 45000
        print(f"PASS: TA={ta:.0f}µs <= 45000µs (3GPP limit)")

    def test_ta_positive(self):
        """Timing advance should always be positive."""
        for elev in [10, 30, 45, 60, 90]:
            ta = self.mgr.calculate_timing_advance(float(elev))
            assert ta > 0
        print("PASS: TA positive for all elevation angles")

    def test_ta_monotonic_decrease(self):
        """TA should decrease as elevation increases (shorter path)."""
        elevations = [10, 30, 45, 60, 90]
        ta_values = [self.mgr.calculate_timing_advance(float(e)) for e in elevations]
        for i in range(len(ta_values) - 1):
            assert ta_values[i] >= ta_values[i + 1]
        print(f"PASS: TA monotonically decreases with elevation")


class TestDopplerShift:
    """White-box tests for Doppler shift compensation."""

    def setup_method(self):
        self.mgr = HybridConnectivityManager()

    def test_max_doppler_at_low_elevation(self):
        """Maximum Doppler shift occurs at lowest elevation angle."""
        doppler_low = self.mgr.calculate_doppler_shift(10.0)
        doppler_high = self.mgr.calculate_doppler_shift(90.0)
        assert abs(doppler_low) > abs(doppler_high)
        print(f"PASS: Doppler at 10° ({doppler_low:.0f}Hz) > at 90° ({doppler_high:.0f}Hz)")

    def test_zero_doppler_at_zenith(self):
        """Doppler shift should be near zero at 90° (satellite directly overhead)."""
        doppler = self.mgr.calculate_doppler_shift(90.0)
        assert abs(doppler) < 100  # Near zero
        print(f"PASS: Doppler at zenith = {doppler:.2f} Hz (near zero)")

    def test_doppler_positive(self):
        """Doppler shift should be positive (approaching satellite)."""
        doppler = self.mgr.calculate_doppler_shift(45.0)
        assert doppler > 0
        print(f"PASS: Doppler at 45° = {doppler:.0f} Hz (positive)")

    def test_doppler_reasonable_range(self):
        """Doppler for LEO at 2GHz should be in kHz range."""
        doppler = self.mgr.calculate_doppler_shift(10.0)
        assert 10000 < doppler < 100000  # 10-100 kHz range
        print(f"PASS: Doppler = {doppler:.0f} Hz (within expected kHz range)")


class TestHandoverLogging:
    """Tests for handover event recording."""

    def setup_method(self):
        self.mgr = HybridConnectivityManager()

    def test_handover_recorded_on_switch(self):
        """Switching from 5G to satellite should record handover event."""
        # Start in 5G
        self.mgr.evaluate_and_switch(rssi_5g=-75.0, rssi_ntn=-85.0)
        # Switch to satellite
        self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-85.0)
        summary = self.mgr.get_handover_summary()
        assert summary['total_handovers'] >= 1
        print(f"PASS: Handover recorded — total={summary['total_handovers']}")

    def test_handover_summary_stats(self):
        """Handover summary should include TA and Doppler stats."""
        self.mgr.evaluate_and_switch(rssi_5g=-75.0, rssi_ntn=-85.0)
        self.mgr.evaluate_and_switch(rssi_5g=-95.0, rssi_ntn=-85.0)
        summary = self.mgr.get_handover_summary()
        assert 'avg_timing_advance_us' in summary
        assert 'avg_doppler_shift_hz' in summary
        assert summary['success_rate'] == 100.0
        print(f"PASS: Handover summary — TA={summary['avg_timing_advance_us']}µs")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
