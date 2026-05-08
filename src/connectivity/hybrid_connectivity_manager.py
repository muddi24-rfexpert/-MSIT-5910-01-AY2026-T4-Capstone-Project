"""
Hybrid Connectivity Manager — 5G + Satellite NTN
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 2.0 | Date: May 8, 2026

Unit 5 Enhancement: Added timing advance management for NTN handover
and Doppler shift compensation for LEO satellite connectivity.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
import math


class ConnectivityMode(Enum):
    FIVE_G = "5G"
    SATELLITE_NTN = "SATELLITE_NTN"
    OFFLINE = "OFFLINE"


@dataclass
class ConnectivityStatus:
    mode: ConnectivityMode
    latency_ms: float
    rssi_dbm: float
    bandwidth_mbps: float
    is_urllc: bool


@dataclass
class HandoverEvent:
    """Records a connectivity handover event."""
    from_mode: ConnectivityMode
    to_mode: ConnectivityMode
    timing_advance_us: float    # Timing advance in microseconds
    doppler_shift_hz: float     # Doppler compensation applied
    handover_latency_ms: float  # Time taken for handover
    success: bool


class HybridConnectivityManager:
    """
    Manages hybrid 5G + LEO Satellite NTN connectivity.
    Implements automatic failover per 3GPP Release 17 NTN specifications.

    5G URLLC target: < 10ms latency
    LEO Satellite fallback target: < 50ms latency

    Unit 5: Added timing advance (TA) management for NTN handover
    and Doppler shift compensation per 3GPP TR 38.821.
    """

    # Per 3GPP TS 38.300 and TR 38.821
    URLLC_LATENCY_TARGET_MS = 10
    NTN_LATENCY_TARGET_MS = 50
    FIVE_G_MIN_RSSI_DBM = -90
    NTN_MIN_RSSI_DBM = -100

    # LEO Satellite parameters (per 3GPP TR 38.821)
    LEO_ALTITUDE_KM = 600           # Typical LEO orbit altitude
    LEO_ORBITAL_VELOCITY_KMS = 7.56 # km/s at 600km altitude
    CARRIER_FREQUENCY_GHZ = 2.0     # S-band NTN carrier
    SPEED_OF_LIGHT_KMS = 299792.458 # km/s
    MAX_TIMING_ADVANCE_US = 45000   # Max TA for LEO (3GPP limit)

    def __init__(self):
        self.current_mode = ConnectivityMode.FIVE_G
        self.failover_count = 0
        self.handover_log: List[HandoverEvent] = []
        self.connection_log = []

    def evaluate_and_switch(self, rssi_5g: Optional[float], rssi_ntn: Optional[float]) -> ConnectivityStatus:
        """
        Evaluate signal quality and switch connectivity mode if needed.
        5G is always preferred. NTN is fallback. Offline if both unavailable.

        Args:
            rssi_5g: 5G signal strength in dBm (None if unavailable)
            rssi_ntn: Satellite signal strength in dBm (None if unavailable)

        Returns:
            ConnectivityStatus with current connection parameters
        """
        previous_mode = self.current_mode

        if rssi_5g and rssi_5g > self.FIVE_G_MIN_RSSI_DBM:
            self.current_mode = ConnectivityMode.FIVE_G
            status = ConnectivityStatus(
                mode=ConnectivityMode.FIVE_G,
                latency_ms=8.5,   # Typical 5G URLLC latency
                rssi_dbm=rssi_5g,
                bandwidth_mbps=1000.0,
                is_urllc=True
            )
        elif rssi_ntn and rssi_ntn > self.NTN_MIN_RSSI_DBM:
            self.current_mode = ConnectivityMode.SATELLITE_NTN
            self.failover_count += 1
            status = ConnectivityStatus(
                mode=ConnectivityMode.SATELLITE_NTN,
                latency_ms=35.0,  # Typical LEO satellite latency
                rssi_dbm=rssi_ntn,
                bandwidth_mbps=100.0,
                is_urllc=False
            )
        else:
            self.current_mode = ConnectivityMode.OFFLINE
            status = ConnectivityStatus(
                mode=ConnectivityMode.OFFLINE,
                latency_ms=0.0,
                rssi_dbm=0.0,
                bandwidth_mbps=0.0,
                is_urllc=False
            )

        # Record handover if mode changed
        if previous_mode != self.current_mode and previous_mode != ConnectivityMode.OFFLINE:
            self._record_handover(previous_mode, self.current_mode)

        return status

    def calculate_timing_advance(self, satellite_elevation_deg: float) -> float:
        """
        Calculate timing advance for NTN communication based on satellite elevation.
        Per 3GPP TR 38.821, TA compensates for propagation delay to LEO satellite.

        Algorithm:
            1. Convert elevation angle to slant range
            2. Calculate round-trip propagation delay
            3. Convert to timing advance in microseconds

        Args:
            satellite_elevation_deg: Satellite elevation angle (10-90 degrees)

        Returns:
            Timing advance in microseconds, clamped to 3GPP maximum
        """
        # Validate elevation angle
        elevation_deg = max(10.0, min(90.0, satellite_elevation_deg))
        elevation_rad = math.radians(elevation_deg)

        # Earth radius in km
        earth_radius_km = 6371.0

        # Calculate slant range using geometry
        # slant_range = -R*sin(el) + sqrt((R*sin(el))^2 + 2*R*h + h^2)
        r = earth_radius_km
        h = self.LEO_ALTITUDE_KM
        sin_el = math.sin(elevation_rad)

        slant_range_km = (
            -r * sin_el +
            math.sqrt((r * sin_el) ** 2 + 2 * r * h + h ** 2)
        )

        # Round-trip propagation delay
        round_trip_delay_s = (2 * slant_range_km) / self.SPEED_OF_LIGHT_KMS

        # Convert to microseconds
        timing_advance_us = round_trip_delay_s * 1e6

        # Clamp to 3GPP maximum
        return min(timing_advance_us, self.MAX_TIMING_ADVANCE_US)

    def calculate_doppler_shift(self, satellite_elevation_deg: float) -> float:
        """
        Calculate Doppler frequency shift for LEO satellite communication.
        Maximum Doppler occurs at low elevation angles when satellite moves
        fastest relative to the ground station.

        Per 3GPP TR 38.821 Section 6.1.3:
            f_doppler = (v_sat * f_carrier * cos(elevation)) / c

        Args:
            satellite_elevation_deg: Satellite elevation angle (10-90 degrees)

        Returns:
            Doppler shift in Hz (positive = approaching, negative = receding)
        """
        elevation_deg = max(10.0, min(90.0, satellite_elevation_deg))
        elevation_rad = math.radians(elevation_deg)

        # Doppler shift formula
        v_sat = self.LEO_ORBITAL_VELOCITY_KMS * 1000  # Convert to m/s
        f_carrier = self.CARRIER_FREQUENCY_GHZ * 1e9   # Convert to Hz
        c = self.SPEED_OF_LIGHT_KMS * 1000             # Convert to m/s

        doppler_hz = (v_sat * f_carrier * math.cos(elevation_rad)) / c

        return round(doppler_hz, 2)

    def _record_handover(self, from_mode: ConnectivityMode, to_mode: ConnectivityMode) -> None:
        """Record a handover event with timing advance and Doppler compensation."""
        # Use typical elevation of 45 degrees for handover calculations
        ta = self.calculate_timing_advance(45.0)
        doppler = self.calculate_doppler_shift(45.0)

        event = HandoverEvent(
            from_mode=from_mode,
            to_mode=to_mode,
            timing_advance_us=round(ta, 2),
            doppler_shift_hz=doppler,
            handover_latency_ms=12.5,  # Typical handover latency
            success=True
        )
        self.handover_log.append(event)

    def get_failover_stats(self) -> dict:
        """Get connectivity failover statistics."""
        return {
            'total_failovers': self.failover_count,
            'current_mode': self.current_mode.value,
            'handover_events': len(self.handover_log)
        }

    def get_handover_summary(self) -> dict:
        """Get detailed handover performance summary."""
        if not self.handover_log:
            return {'total_handovers': 0}

        avg_ta = sum(h.timing_advance_us for h in self.handover_log) / len(self.handover_log)
        avg_doppler = sum(h.doppler_shift_hz for h in self.handover_log) / len(self.handover_log)
        success_rate = sum(1 for h in self.handover_log if h.success) / len(self.handover_log)

        return {
            'total_handovers': len(self.handover_log),
            'avg_timing_advance_us': round(avg_ta, 2),
            'avg_doppler_shift_hz': round(avg_doppler, 2),
            'success_rate': round(success_rate * 100, 1),
            'avg_handover_latency_ms': 12.5
        }
