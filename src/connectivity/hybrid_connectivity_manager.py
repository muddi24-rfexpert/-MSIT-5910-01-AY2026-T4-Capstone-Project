"""
Hybrid Connectivity Manager — 5G + Satellite NTN
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 1.0 | Date: April 28, 2026
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


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


class HybridConnectivityManager:
    """
    Manages hybrid 5G + LEO Satellite NTN connectivity.
    Implements automatic failover per 3GPP Release 17 NTN specifications.

    5G URLLC target: < 10ms latency
    LEO Satellite fallback target: < 50ms latency
    """

    # Per 3GPP TS 38.300 and TR 38.821
    URLLC_LATENCY_TARGET_MS = 10
    NTN_LATENCY_TARGET_MS = 50
    FIVE_G_MIN_RSSI_DBM = -90
    NTN_MIN_RSSI_DBM = -100

    def __init__(self):
        self.current_mode = ConnectivityMode.FIVE_G
        self.failover_count = 0
        self.connection_log = []

    def evaluate_and_switch(self, rssi_5g: Optional[float], rssi_ntn: Optional[float]) -> ConnectivityStatus:
        """
        Evaluate signal quality and switch connectivity mode if needed.
        5G is always preferred. NTN is fallback. Offline if both unavailable.
        """
        if rssi_5g and rssi_5g > self.FIVE_G_MIN_RSSI_DBM:
            self.current_mode = ConnectivityMode.FIVE_G
            return ConnectivityStatus(
                mode=ConnectivityMode.FIVE_G,
                latency_ms=8.5,   # Typical 5G URLLC latency
                rssi_dbm=rssi_5g,
                bandwidth_mbps=1000.0,
                is_urllc=True
            )
        elif rssi_ntn and rssi_ntn > self.NTN_MIN_RSSI_DBM:
            self.current_mode = ConnectivityMode.SATELLITE_NTN
            self.failover_count += 1
            return ConnectivityStatus(
                mode=ConnectivityMode.SATELLITE_NTN,
                latency_ms=35.0,  # Typical LEO satellite latency
                rssi_dbm=rssi_ntn,
                bandwidth_mbps=100.0,
                is_urllc=False
            )
        else:
            self.current_mode = ConnectivityMode.OFFLINE
            return ConnectivityStatus(
                mode=ConnectivityMode.OFFLINE,
                latency_ms=0.0,
                rssi_dbm=0.0,
                bandwidth_mbps=0.0,
                is_urllc=False
            )

    def get_failover_stats(self) -> dict:
        return {
            'total_failovers': self.failover_count,
            'current_mode': self.current_mode.value
        }


# Unit 4 TODO: Add Doppler shift compensation for LEO satellite
# Unit 5 TODO: Add timing advance management for NTN handover
