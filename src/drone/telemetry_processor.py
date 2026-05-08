"""
Drone Telemetry Processor Module
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 2.0 | Date: May 8, 2026

Unit 5 Enhancement: Added GPS path optimization using nearest-neighbor
heuristic for efficient drone flight path planning.
"""

import json
import time
import math
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class TelemetryData:
    """Represents a single drone telemetry reading."""
    drone_id: str
    timestamp: float
    latitude: float
    longitude: float
    altitude: float          # meters
    battery_level: float     # percentage
    rssi_5g: Optional[float] # dBm - 5G signal strength
    rssi_satellite: Optional[float]  # dBm - satellite signal
    connectivity_mode: str   # '5G', 'SATELLITE', 'OFFLINE'
    sensor_data: dict        # multispectral, thermal, lidar readings


@dataclass
class OptimizedPath:
    """Result of GPS path optimization."""
    waypoints: List[Tuple[float, float]]  # Ordered (lat, lon) pairs
    total_distance_km: float
    estimated_flight_time_min: float
    energy_savings_pct: float             # vs. unoptimized path
    original_distance_km: float


class TelemetryProcessor:
    """
    Processes real-time telemetry data from agricultural drones.
    Handles 5G and satellite connectivity switching.

    Unit 5: Added GPS path optimization using nearest-neighbor algorithm
    to minimize flight distance and maximize battery efficiency.
    """

    # RSSI thresholds for connectivity decisions
    RSSI_5G_THRESHOLD = -90      # dBm - minimum acceptable 5G signal
    RSSI_SAT_THRESHOLD = -100    # dBm - minimum acceptable satellite signal

    # Drone flight parameters
    DRONE_SPEED_KMH = 45.0       # Average drone cruise speed
    EARTH_RADIUS_KM = 6371.0     # For Haversine distance calculation

    def __init__(self, drone_id: str):
        self.drone_id = drone_id
        self.telemetry_buffer: List[TelemetryData] = []
        self.current_mode = '5G'

    def process_telemetry(self, raw_data: dict) -> TelemetryData:
        """
        Process raw sensor data into structured telemetry.
        Automatically selects connectivity mode based on signal strength.

        Args:
            raw_data: Dictionary with lat, lon, alt, battery, rssi_5g,
                      rssi_sat, and sensors fields

        Returns:
            Structured TelemetryData object
        """
        telemetry = TelemetryData(
            drone_id=self.drone_id,
            timestamp=time.time(),
            latitude=raw_data.get('lat', 0.0),
            longitude=raw_data.get('lon', 0.0),
            altitude=raw_data.get('alt', 0.0),
            battery_level=raw_data.get('battery', 100.0),
            rssi_5g=raw_data.get('rssi_5g'),
            rssi_satellite=raw_data.get('rssi_sat'),
            connectivity_mode=self._select_connectivity(raw_data),
            sensor_data=raw_data.get('sensors', {})
        )
        self.telemetry_buffer.append(telemetry)
        return telemetry

    def _select_connectivity(self, raw_data: dict) -> str:
        """
        Select best connectivity mode: 5G primary, satellite fallback.
        Implements hybrid connectivity logic per 3GPP NTN specifications.
        """
        rssi_5g = raw_data.get('rssi_5g')
        rssi_sat = raw_data.get('rssi_sat')

        if rssi_5g and rssi_5g > self.RSSI_5G_THRESHOLD:
            return '5G'
        elif rssi_sat and rssi_sat > self.RSSI_SAT_THRESHOLD:
            return 'SATELLITE'
        else:
            return 'OFFLINE'

    def haversine_distance(self, lat1: float, lon1: float,
                           lat2: float, lon2: float) -> float:
        """
        Calculate great-circle distance between two GPS coordinates
        using the Haversine formula.

        Args:
            lat1, lon1: First point coordinates in degrees
            lat2, lon2: Second point coordinates in degrees

        Returns:
            Distance in kilometers
        """
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return self.EARTH_RADIUS_KM * c

    def optimize_flight_path(self, waypoints: List[Tuple[float, float]],
                             start_point: Tuple[float, float] = None) -> OptimizedPath:
        """
        Optimize drone flight path using nearest-neighbor heuristic.
        Minimizes total travel distance to reduce battery consumption
        and flight time.

        Algorithm:
            1. Start from the given start point (or first waypoint)
            2. At each step, visit the nearest unvisited waypoint
            3. Calculate total optimized distance
            4. Compare with original sequential distance for savings

        Args:
            waypoints: List of (latitude, longitude) tuples to visit
            start_point: Optional starting position (defaults to first waypoint)

        Returns:
            OptimizedPath with ordered waypoints and efficiency metrics
        """
        if not waypoints:
            return OptimizedPath(
                waypoints=[],
                total_distance_km=0.0,
                estimated_flight_time_min=0.0,
                energy_savings_pct=0.0,
                original_distance_km=0.0
            )

        if len(waypoints) == 1:
            return OptimizedPath(
                waypoints=waypoints,
                total_distance_km=0.0,
                estimated_flight_time_min=0.0,
                energy_savings_pct=0.0,
                original_distance_km=0.0
            )

        # Calculate original sequential distance
        original_distance = 0.0
        for i in range(len(waypoints) - 1):
            original_distance += self.haversine_distance(
                waypoints[i][0], waypoints[i][1],
                waypoints[i + 1][0], waypoints[i + 1][1]
            )

        # Nearest-neighbor optimization
        if start_point:
            current = start_point
        else:
            current = waypoints[0]

        unvisited = list(waypoints)
        if start_point and start_point in unvisited:
            unvisited.remove(start_point)
        elif not start_point:
            unvisited.remove(waypoints[0])

        optimized = [current]
        total_distance = 0.0

        while unvisited:
            # Find nearest unvisited waypoint
            nearest = None
            nearest_dist = float('inf')

            for wp in unvisited:
                dist = self.haversine_distance(
                    current[0], current[1], wp[0], wp[1]
                )
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest = wp

            total_distance += nearest_dist
            current = nearest
            optimized.append(current)
            unvisited.remove(nearest)

        # Calculate savings
        if original_distance > 0:
            savings_pct = ((original_distance - total_distance) / original_distance) * 100
        else:
            savings_pct = 0.0

        # Estimate flight time
        flight_time_min = (total_distance / self.DRONE_SPEED_KMH) * 60

        return OptimizedPath(
            waypoints=optimized,
            total_distance_km=round(total_distance, 4),
            estimated_flight_time_min=round(flight_time_min, 2),
            energy_savings_pct=round(max(0.0, savings_pct), 1),
            original_distance_km=round(original_distance, 4)
        )

    def get_buffer_summary(self) -> dict:
        """Return summary statistics of buffered telemetry."""
        if not self.telemetry_buffer:
            return {}
        return {
            'total_readings': len(self.telemetry_buffer),
            'drone_id': self.drone_id,
            'connectivity_modes': list(set(t.connectivity_mode for t in self.telemetry_buffer))
        }
