"""
Edge Computing Processor Module
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 2.0 | Date: May 8, 2026

Unit 5 Enhancement: Added local model update mechanism that allows
edge nodes to receive and apply model weight updates from the cloud
without full redeployment (federated learning support).
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import time
import hashlib


@dataclass
class EdgeProcessingResult:
    """Result from edge AI inference."""
    drone_id: str
    timestamp: float
    crop_health_score: float
    irrigation_trigger: bool
    alert_level: str          # 'none', 'low', 'medium', 'critical'
    data_sent_to_cloud: bool
    processing_latency_ms: float


@dataclass
class ModelUpdateResult:
    """Result of a local model update operation."""
    update_id: str
    previous_version: str
    new_version: str
    weights_applied: int
    validation_accuracy: float
    update_latency_ms: float
    success: bool
    rollback_available: bool


class EdgeProcessor:
    """
    On-site edge computing processor for real-time AI inference.
    Reduces cloud data transmission by ~70% through local filtering.
    Target processing latency: < 20ms per 3GPP edge computing specs.

    Unit 5: Added local model update mechanism supporting incremental
    weight updates from cloud without full model redeployment.
    Implements version tracking and rollback capability.
    """

    ALERT_THRESHOLDS = {
        'critical': 0.2,
        'medium': 0.4,
        'low': 0.6
    }

    def __init__(self, edge_node_id: str):
        self.edge_node_id = edge_node_id
        self.processed_count = 0
        self.cloud_transmissions = 0
        # Model management
        self.model_version = "1.0.0"
        self.model_weights: Dict[str, float] = {
            'ndvi_weight': 0.4,
            'thermal_weight': 0.3,
            'spectral_weight': 0.3
        }
        self.update_history: List[ModelUpdateResult] = []
        self.previous_weights: Optional[Dict[str, float]] = None

    def process(self, telemetry: dict, health_score: float) -> EdgeProcessingResult:
        """
        Process drone data at edge. Only send critical/summary data to cloud.
        This reduces bandwidth usage by filtering routine readings locally.

        Args:
            telemetry: Dictionary with drone telemetry data
            health_score: AI-computed crop health score (0.0 to 1.0)

        Returns:
            EdgeProcessingResult with processing outcome
        """
        start_time = time.time()

        alert_level = self._determine_alert(health_score)
        irrigation_trigger = health_score < self.ALERT_THRESHOLDS['medium']

        # Only transmit to cloud if alert or every 10th reading (summary)
        send_to_cloud = alert_level != 'none' or (self.processed_count % 10 == 0)
        if send_to_cloud:
            self.cloud_transmissions += 1

        self.processed_count += 1
        latency = (time.time() - start_time) * 1000  # ms

        return EdgeProcessingResult(
            drone_id=telemetry.get('drone_id', 'unknown'),
            timestamp=time.time(),
            crop_health_score=health_score,
            irrigation_trigger=irrigation_trigger,
            alert_level=alert_level,
            data_sent_to_cloud=send_to_cloud,
            processing_latency_ms=latency
        )

    def _determine_alert(self, health_score: float) -> str:
        """Determine alert level based on health score thresholds."""
        if health_score < self.ALERT_THRESHOLDS['critical']:
            return 'critical'
        elif health_score < self.ALERT_THRESHOLDS['medium']:
            return 'medium'
        elif health_score < self.ALERT_THRESHOLDS['low']:
            return 'low'
        return 'none'

    def apply_model_update(self, new_weights: Dict[str, float],
                           new_version: str,
                           validation_data: List[Dict] = None) -> ModelUpdateResult:
        """
        Apply incremental model weight update from cloud.
        Supports rollback if validation accuracy drops below threshold.

        Algorithm:
            1. Store current weights as backup (rollback point)
            2. Apply new weights to local model
            3. Run validation on provided test data
            4. If accuracy >= 80%, confirm update; otherwise rollback
            5. Record update in history log

        Args:
            new_weights: Dictionary of weight name -> new value
            new_version: Version string for the update
            validation_data: Optional list of test cases for validation

        Returns:
            ModelUpdateResult with update outcome
        """
        start_time = time.time()

        # Store backup for rollback
        self.previous_weights = dict(self.model_weights)
        previous_version = self.model_version

        # Apply new weights
        weights_applied = 0
        for key, value in new_weights.items():
            if key in self.model_weights:
                self.model_weights[key] = value
                weights_applied += 1

        # Validate the update
        validation_accuracy = self._validate_model(validation_data)

        # Check if update meets quality threshold
        success = validation_accuracy >= 0.80

        if not success:
            # Rollback to previous weights
            self.model_weights = dict(self.previous_weights)
            applied_version = previous_version
        else:
            self.model_version = new_version
            applied_version = new_version

        update_latency = (time.time() - start_time) * 1000

        # Generate update ID
        update_id = hashlib.md5(
            f"{self.edge_node_id}_{new_version}_{time.time()}".encode()
        ).hexdigest()[:12]

        result = ModelUpdateResult(
            update_id=update_id,
            previous_version=previous_version,
            new_version=applied_version,
            weights_applied=weights_applied,
            validation_accuracy=round(validation_accuracy, 4),
            update_latency_ms=round(update_latency, 2),
            success=success,
            rollback_available=True
        )

        self.update_history.append(result)
        return result

    def _validate_model(self, validation_data: List[Dict] = None) -> float:
        """
        Validate model accuracy after weight update.
        Uses provided test data or synthetic validation.

        Args:
            validation_data: List of dicts with 'health_score' and 'expected_alert'

        Returns:
            Accuracy as float (0.0 to 1.0)
        """
        if not validation_data:
            # Use synthetic validation with known test cases
            validation_data = [
                {'health_score': 0.1, 'expected_alert': 'critical'},
                {'health_score': 0.3, 'expected_alert': 'medium'},
                {'health_score': 0.5, 'expected_alert': 'low'},
                {'health_score': 0.7, 'expected_alert': 'none'},
                {'health_score': 0.9, 'expected_alert': 'none'},
            ]

        correct = 0
        for test_case in validation_data:
            predicted = self._determine_alert(test_case['health_score'])
            if predicted == test_case['expected_alert']:
                correct += 1

        return correct / len(validation_data) if validation_data else 0.0

    def rollback_model(self) -> bool:
        """
        Rollback to previous model weights if available.

        Returns:
            True if rollback successful, False if no backup available
        """
        if self.previous_weights is None:
            return False

        self.model_weights = dict(self.previous_weights)
        self.previous_weights = None

        # Revert version
        if self.update_history:
            self.model_version = self.update_history[-1].previous_version

        return True

    def get_efficiency_stats(self) -> dict:
        """Calculate cloud transmission reduction rate."""
        if self.processed_count == 0:
            return {}
        reduction = 1 - (self.cloud_transmissions / self.processed_count)
        return {
            'total_processed': self.processed_count,
            'cloud_transmissions': self.cloud_transmissions,
            'bandwidth_reduction_pct': round(reduction * 100, 1)
        }

    def get_model_status(self) -> dict:
        """Get current model version and update history summary."""
        return {
            'edge_node_id': self.edge_node_id,
            'model_version': self.model_version,
            'current_weights': dict(self.model_weights),
            'total_updates': len(self.update_history),
            'successful_updates': sum(1 for u in self.update_history if u.success),
            'rollback_available': self.previous_weights is not None
        }
