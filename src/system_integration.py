"""
Full System Integration Module
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 3.0 | Date: May 15, 2026

Unit 6: Integrates all modules into a unified pipeline demonstrating
inter-module communication: Drone -> Connectivity -> AI -> Edge -> Cloud
"""

import sys
import os
import time
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from drone.telemetry_processor import TelemetryProcessor, TelemetryData
from ai_models.crop_health_classifier import CropHealthClassifier, CropHealthResult
from connectivity.hybrid_connectivity_manager import (
    HybridConnectivityManager, ConnectivityMode, ConnectivityStatus
)
from edge.edge_processor import EdgeProcessor, EdgeProcessingResult


class SystemIntegrationPipeline:
    """
    Unified system integration pipeline that orchestrates all modules.
    Implements the complete data flow:
        Drone Telemetry -> Connectivity Check -> AI Classification ->
        Edge Processing -> Cloud Decision

    This class demonstrates inter-module communication through
    structured data passing between layers.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize all system modules with configuration.

        Args:
            config: Optional configuration dictionary overriding defaults
        """
        self.config = config or self._default_config()

        # Initialize modules (inter-module dependencies)
        self.telemetry_processors: Dict[str, TelemetryProcessor] = {}
        self.classifier = CropHealthClassifier()
        self.connectivity_mgr = HybridConnectivityManager()
        self.edge_processor = EdgeProcessor(
            self.config.get('edge_node_id', 'EDGE-NODE-01')
        )

        # Pipeline metrics
        self.pipeline_runs = 0
        self.total_latency_ms = 0.0
        self.alerts_generated = 0
        self.cloud_transmissions = 0

    def _default_config(self) -> Dict[str, Any]:
        """Default system configuration matching system_config.yaml."""
        return {
            'edge_node_id': 'EDGE-NODE-01',
            'drone_count': 5,
            'urllc_latency_target_ms': 10,
            'ntn_latency_target_ms': 50,
            'ndvi_healthy_threshold': 0.6,
            'target_accuracy_pct': 90,
            'cloud_sync_interval': 10,
        }

    def get_or_create_processor(self, drone_id: str) -> TelemetryProcessor:
        """Get existing or create new telemetry processor for a drone."""
        if drone_id not in self.telemetry_processors:
            self.telemetry_processors[drone_id] = TelemetryProcessor(drone_id)
        return self.telemetry_processors[drone_id]

    def process_drone_reading(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the full integration pipeline for a single drone reading.
        This is the core inter-module communication method.

        Pipeline Flow:
            1. Telemetry Processing (Drone Layer)
            2. Connectivity Evaluation (Connectivity Layer)
            3. AI Health Classification (AI Layer)
            4. Edge Processing & Cloud Decision (Edge Layer)
            5. Trend Analysis (Predictive Analytics)

        Args:
            raw_data: Raw sensor data from drone including:
                - drone_id: Drone identifier
                - lat, lon, alt: GPS coordinates
                - battery: Battery percentage
                - rssi_5g, rssi_sat: Signal strengths
                - nir, red: Spectral band values
                - thermal: Temperature reading
                - zone_id: Field zone identifier

        Returns:
            Complete pipeline result dictionary with all layer outputs
        """
        pipeline_start = time.time()

        drone_id = raw_data.get('drone_id', 'UNKNOWN')
        zone_id = raw_data.get('zone_id', 'zone-1')

        # ── LAYER 1: Telemetry Processing ────────────────────────────
        processor = self.get_or_create_processor(drone_id)
        telemetry = processor.process_telemetry(raw_data)

        # ── LAYER 2: Connectivity Evaluation ─────────────────────────
        conn_status = self.connectivity_mgr.evaluate_and_switch(
            rssi_5g=raw_data.get('rssi_5g'),
            rssi_ntn=raw_data.get('rssi_sat')
        )

        # Calculate NTN parameters if on satellite
        timing_advance = None
        doppler_shift = None
        if conn_status.mode == ConnectivityMode.SATELLITE_NTN:
            elevation = raw_data.get('satellite_elevation', 45.0)
            timing_advance = self.connectivity_mgr.calculate_timing_advance(elevation)
            doppler_shift = self.connectivity_mgr.calculate_doppler_shift(elevation)

        # ── LAYER 3: AI Classification ───────────────────────────────
        nir = raw_data.get('nir', 0.5)
        red = raw_data.get('red', 0.3)
        thermal = raw_data.get('thermal')

        ndvi = self.classifier.calculate_ndvi(nir, red)
        health_result = self.classifier.classify_health(float(ndvi), thermal)

        # Record for trend analysis
        self.classifier.record_ndvi(zone_id, float(ndvi))
        trend_result = self.classifier.analyze_trend(zone_id)

        # ── LAYER 4: Edge Processing ─────────────────────────────────
        edge_result = self.edge_processor.process(
            {'drone_id': drone_id, 'zone_id': zone_id},
            health_result.health_score
        )

        # ── Pipeline Metrics ─────────────────────────────────────────
        pipeline_latency_ms = (time.time() - pipeline_start) * 1000
        self.pipeline_runs += 1
        self.total_latency_ms += pipeline_latency_ms

        if edge_result.alert_level != 'none':
            self.alerts_generated += 1
        if edge_result.data_sent_to_cloud:
            self.cloud_transmissions += 1

        # ── Assemble Result ──────────────────────────────────────────
        return {
            'pipeline_run': self.pipeline_runs,
            'drone_id': drone_id,
            'zone_id': zone_id,
            'telemetry': {
                'latitude': telemetry.latitude,
                'longitude': telemetry.longitude,
                'altitude': telemetry.altitude,
                'battery': telemetry.battery_level,
                'connectivity_mode': telemetry.connectivity_mode,
            },
            'connectivity': {
                'mode': conn_status.mode.value,
                'latency_ms': conn_status.latency_ms,
                'bandwidth_mbps': conn_status.bandwidth_mbps,
                'is_urllc': conn_status.is_urllc,
                'timing_advance_us': timing_advance,
                'doppler_shift_hz': doppler_shift,
            },
            'ai_classification': {
                'ndvi': round(float(ndvi), 4),
                'health_score': health_result.health_score,
                'stress_detected': health_result.stress_detected,
                'stress_type': health_result.stress_type,
                'confidence': health_result.confidence,
                'recommendation': health_result.recommendation,
            },
            'edge_processing': {
                'alert_level': edge_result.alert_level,
                'irrigation_trigger': edge_result.irrigation_trigger,
                'sent_to_cloud': edge_result.data_sent_to_cloud,
                'processing_latency_ms': edge_result.processing_latency_ms,
            },
            'trend_analysis': {
                'direction': trend_result.trend_direction if trend_result else None,
                'slope': trend_result.slope if trend_result else None,
                'early_warning': trend_result.early_warning if trend_result else None,
            },
            'pipeline_metrics': {
                'total_latency_ms': round(pipeline_latency_ms, 3),
                'cumulative_runs': self.pipeline_runs,
            }
        }

    def process_batch(self, readings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a batch of drone readings through the full pipeline.

        Args:
            readings: List of raw data dictionaries

        Returns:
            List of pipeline results
        """
        results = []
        for reading in readings:
            result = self.process_drone_reading(reading)
            results.append(result)
        return results

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive system performance metrics.

        Returns:
            Dictionary with throughput, latency, accuracy, and efficiency metrics
        """
        avg_latency = (self.total_latency_ms / self.pipeline_runs
                       if self.pipeline_runs > 0 else 0.0)

        edge_stats = self.edge_processor.get_efficiency_stats()
        conn_stats = self.connectivity_mgr.get_failover_stats()
        handover_stats = self.connectivity_mgr.get_handover_summary()

        return {
            'throughput': {
                'total_readings_processed': self.pipeline_runs,
                'readings_per_second': round(
                    self.pipeline_runs / (self.total_latency_ms / 1000)
                    if self.total_latency_ms > 0 else 0, 1
                ),
            },
            'latency': {
                'average_pipeline_ms': round(avg_latency, 3),
                'target_5g_ms': self.config.get('urllc_latency_target_ms', 10),
                'target_ntn_ms': self.config.get('ntn_latency_target_ms', 50),
            },
            'connectivity': {
                'failovers': conn_stats['total_failovers'],
                'current_mode': conn_stats['current_mode'],
                'handover_summary': handover_stats,
            },
            'edge_efficiency': edge_stats,
            'alerts': {
                'total_alerts': self.alerts_generated,
                'cloud_transmissions': self.cloud_transmissions,
            }
        }


def run_integration_demo():
    """Run a complete system integration demonstration."""
    print("=" * 70)
    print("  SYSTEM INTEGRATION PIPELINE — Full Demo")
    print("  5G & Satellite-Based AI Drone System for Precision Agriculture")
    print("=" * 70)

    # Initialize pipeline
    pipeline = SystemIntegrationPipeline()

    # Simulated field data (9 readings across 4 zones)
    field_readings = [
        {'drone_id': 'DRONE-01', 'lat': 39.7392, 'lon': -104.9903, 'alt': 50.0,
         'battery': 92.0, 'rssi_5g': -75.0, 'rssi_sat': -95.0,
         'nir': 0.82, 'red': 0.18, 'thermal': 28.0, 'zone_id': 'zone-1'},
        {'drone_id': 'DRONE-01', 'lat': 39.7395, 'lon': -104.9900, 'alt': 50.0,
         'battery': 90.0, 'rssi_5g': -78.0, 'rssi_sat': -94.0,
         'nir': 0.79, 'red': 0.21, 'thermal': 29.0, 'zone_id': 'zone-1'},
        {'drone_id': 'DRONE-02', 'lat': 39.7400, 'lon': -104.9910, 'alt': 50.0,
         'battery': 88.0, 'rssi_5g': -88.0, 'rssi_sat': -92.0,
         'nir': 0.52, 'red': 0.38, 'thermal': 34.0, 'zone_id': 'zone-2'},
        {'drone_id': 'DRONE-02', 'lat': 39.7403, 'lon': -104.9908, 'alt': 50.0,
         'battery': 85.0, 'rssi_5g': -91.0, 'rssi_sat': -89.0,
         'nir': 0.48, 'red': 0.42, 'thermal': 36.0, 'zone_id': 'zone-2'},
        {'drone_id': 'DRONE-03', 'lat': 39.7410, 'lon': -104.9920, 'alt': 50.0,
         'battery': 82.0, 'rssi_5g': -95.0, 'rssi_sat': -85.0,
         'nir': 0.31, 'red': 0.55, 'thermal': 38.0, 'zone_id': 'zone-3'},
        {'drone_id': 'DRONE-03', 'lat': 39.7413, 'lon': -104.9918, 'alt': 50.0,
         'battery': 80.0, 'rssi_5g': -97.0, 'rssi_sat': -83.0,
         'nir': 0.28, 'red': 0.58, 'thermal': 39.5, 'zone_id': 'zone-3'},
        {'drone_id': 'DRONE-04', 'lat': 39.7420, 'lon': -104.9930, 'alt': 50.0,
         'battery': 78.0, 'rssi_5g': -98.0, 'rssi_sat': -82.0,
         'nir': 0.14, 'red': 0.72, 'thermal': 42.0, 'zone_id': 'zone-4'},
        {'drone_id': 'DRONE-04', 'lat': 39.7423, 'lon': -104.9928, 'alt': 50.0,
         'battery': 75.0, 'rssi_5g': -99.0, 'rssi_sat': -81.0,
         'nir': 0.11, 'red': 0.75, 'thermal': 43.5, 'zone_id': 'zone-4'},
        {'drone_id': 'DRONE-05', 'lat': 39.7392, 'lon': -104.9903, 'alt': 50.0,
         'battery': 95.0, 'rssi_5g': -72.0, 'rssi_sat': -96.0,
         'nir': 0.85, 'red': 0.15, 'thermal': 27.5, 'zone_id': 'zone-1'},
    ]

    # Process all readings
    print("\n[PROCESSING] Running full pipeline on 9 field readings...\n")
    results = pipeline.process_batch(field_readings)

    # Display results
    for r in results:
        mode_icon = "5G" if r['connectivity']['mode'] == '5G' else "SAT"
        alert = r['edge_processing']['alert_level'].upper()
        print(f"  [{mode_icon}] {r['drone_id']} | Zone: {r['zone_id']} | "
              f"NDVI: {r['ai_classification']['ndvi']:.3f} | "
              f"Health: {r['ai_classification']['health_score']:.2f} | "
              f"Alert: {alert} | "
              f"Cloud: {'YES' if r['edge_processing']['sent_to_cloud'] else 'NO'} | "
              f"Latency: {r['pipeline_metrics']['total_latency_ms']:.2f}ms")

    # System metrics
    print("\n" + "=" * 70)
    print("  SYSTEM PERFORMANCE METRICS")
    print("=" * 70)
    metrics = pipeline.get_system_metrics()

    print(f"\n  Throughput:")
    print(f"    Total readings processed : {metrics['throughput']['total_readings_processed']}")
    print(f"    Processing rate           : {metrics['throughput']['readings_per_second']} readings/sec")

    print(f"\n  Latency:")
    print(f"    Average pipeline latency  : {metrics['latency']['average_pipeline_ms']:.3f} ms")
    print(f"    5G URLLC target           : < {metrics['latency']['target_5g_ms']} ms")
    print(f"    NTN fallback target       : < {metrics['latency']['target_ntn_ms']} ms")

    print(f"\n  Edge Efficiency:")
    if metrics['edge_efficiency']:
        print(f"    Bandwidth reduction       : {metrics['edge_efficiency']['bandwidth_reduction_pct']}%")
        print(f"    Cloud transmissions       : {metrics['edge_efficiency']['cloud_transmissions']}")

    print(f"\n  Connectivity:")
    print(f"    Failovers executed        : {metrics['connectivity']['failovers']}")
    print(f"    Current mode              : {metrics['connectivity']['current_mode']}")

    print(f"\n  Alerts:")
    print(f"    Total alerts generated    : {metrics['alerts']['total_alerts']}")

    print("\n" + "=" * 70)
    print("  INTEGRATION PIPELINE COMPLETE")
    print("=" * 70)

    return metrics


if __name__ == "__main__":
    run_integration_demo()
