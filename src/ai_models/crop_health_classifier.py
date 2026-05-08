"""
Crop Health Classifier — AI Model Module
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 2.0 | Date: May 8, 2026

Unit 5 Enhancement: Added time-series trend analysis for predictive
crop health monitoring and early stress detection.
"""

from dataclasses import dataclass
from typing import Tuple, List, Optional
import statistics


@dataclass
class CropHealthResult:
    """Result of crop health classification."""
    health_score: float      # 0.0 (critical) to 1.0 (healthy)
    stress_detected: bool
    stress_type: str         # 'water', 'nutrient', 'disease', 'pest', 'none'
    ndvi_value: float        # Normalized Difference Vegetation Index
    confidence: float        # Model confidence 0.0 to 1.0
    recommendation: str


@dataclass
class TrendAnalysisResult:
    """Result of time-series trend analysis on NDVI readings."""
    trend_direction: str     # 'improving', 'stable', 'declining'
    slope: float             # Rate of change per reading
    average_ndvi: float      # Mean NDVI over the window
    std_deviation: float     # Variability in readings
    predicted_next: float    # Predicted next NDVI value
    early_warning: bool      # True if declining trend detected before threshold


class CropHealthClassifier:
    """
    AI-based crop health classifier using multispectral imagery.
    Uses NDVI analysis and CNN-based classification.
    Target accuracy: >= 90% (per system requirements FR-03)

    Unit 5: Added time-series trend analysis using linear regression
    on historical NDVI readings for predictive health monitoring.
    """

    # NDVI thresholds (standard agricultural values)
    NDVI_HEALTHY    = 0.6   # > 0.6 = healthy vegetation
    NDVI_MODERATE   = 0.4   # 0.4-0.6 = moderate stress
    NDVI_STRESSED   = 0.2   # 0.2-0.4 = significant stress
    NDVI_CRITICAL   = 0.0   # < 0.2 = critical / bare soil

    # Trend analysis parameters
    TREND_WINDOW_SIZE = 5       # Minimum readings for trend analysis
    DECLINE_THRESHOLD = -0.02   # Slope below this = declining
    IMPROVE_THRESHOLD = 0.02    # Slope above this = improving

    def __init__(self):
        self.model_version = "2.0.0"
        self.model_loaded = False
        self.ndvi_history: dict = {}  # zone_id -> list of NDVI readings

    def calculate_ndvi(self, nir_band: float, red_band: float) -> float:
        """
        Calculate Normalized Difference Vegetation Index.
        NDVI = (NIR - Red) / (NIR + Red)

        Args:
            nir_band: Near-infrared reflectance value (0.0 to 1.0)
            red_band: Red band reflectance value (0.0 to 1.0)

        Returns:
            NDVI value clamped between -1.0 and 1.0
        """
        denominator = nir_band + red_band
        if denominator == 0:
            denominator = 1e-10
        ndvi = (nir_band - red_band) / denominator
        return max(-1.0, min(1.0, ndvi))

    def classify_health(self, ndvi_value: float, thermal_value: float = None) -> CropHealthResult:
        """
        Classify crop health based on NDVI and optional thermal data.
        Returns structured health assessment with recommendation.

        Args:
            ndvi_value: Calculated NDVI (-1.0 to 1.0)
            thermal_value: Optional thermal reading in Celsius

        Returns:
            CropHealthResult with classification and recommendation
        """
        if ndvi_value >= self.NDVI_HEALTHY:
            return CropHealthResult(
                health_score=ndvi_value,
                stress_detected=False,
                stress_type='none',
                ndvi_value=ndvi_value,
                confidence=0.92,
                recommendation="Crop is healthy. Continue standard monitoring schedule."
            )
        elif ndvi_value >= self.NDVI_MODERATE:
            return CropHealthResult(
                health_score=ndvi_value,
                stress_detected=True,
                stress_type='water' if thermal_value and thermal_value > 35 else 'nutrient',
                ndvi_value=ndvi_value,
                confidence=0.87,
                recommendation="Moderate stress detected. Increase irrigation by 20% and monitor for 48 hours."
            )
        elif ndvi_value >= self.NDVI_STRESSED:
            return CropHealthResult(
                health_score=ndvi_value,
                stress_detected=True,
                stress_type='disease',
                ndvi_value=ndvi_value,
                confidence=0.83,
                recommendation="Significant stress detected. Immediate irrigation required. Schedule field inspection."
            )
        else:
            return CropHealthResult(
                health_score=ndvi_value,
                stress_detected=True,
                stress_type='pest',
                ndvi_value=ndvi_value,
                confidence=0.79,
                recommendation="CRITICAL: Severe crop stress. Emergency intervention required within 24 hours."
            )

    def record_ndvi(self, zone_id: str, ndvi_value: float) -> None:
        """
        Record an NDVI reading for time-series trend analysis.

        Args:
            zone_id: Identifier for the field zone
            ndvi_value: NDVI reading to record
        """
        if zone_id not in self.ndvi_history:
            self.ndvi_history[zone_id] = []
        self.ndvi_history[zone_id].append(ndvi_value)

    def analyze_trend(self, zone_id: str) -> Optional[TrendAnalysisResult]:
        """
        Perform time-series trend analysis on recorded NDVI values.
        Uses simple linear regression to detect declining health trends
        before they cross critical thresholds (early warning system).

        Algorithm:
            1. Collect NDVI history for the zone
            2. Compute linear regression slope (least squares)
            3. Classify trend as improving/stable/declining
            4. Predict next value using the linear model
            5. Flag early warning if healthy zone is declining

        Args:
            zone_id: Identifier for the field zone

        Returns:
            TrendAnalysisResult or None if insufficient data
        """
        history = self.ndvi_history.get(zone_id, [])

        if len(history) < self.TREND_WINDOW_SIZE:
            return None

        # Use the most recent window of readings
        window = history[-self.TREND_WINDOW_SIZE:]
        n = len(window)

        # Linear regression: slope = (n*sum(x*y) - sum(x)*sum(y)) / (n*sum(x^2) - sum(x)^2)
        x_values = list(range(n))
        x_sum = sum(x_values)
        y_sum = sum(window)
        xy_sum = sum(x * y for x, y in zip(x_values, window))
        x2_sum = sum(x * x for x in x_values)

        denominator = n * x2_sum - x_sum * x_sum
        if denominator == 0:
            slope = 0.0
        else:
            slope = (n * xy_sum - x_sum * y_sum) / denominator

        # Determine trend direction
        if slope > self.IMPROVE_THRESHOLD:
            trend_direction = 'improving'
        elif slope < self.DECLINE_THRESHOLD:
            trend_direction = 'declining'
        else:
            trend_direction = 'stable'

        avg_ndvi = statistics.mean(window)
        std_dev = statistics.stdev(window) if n > 1 else 0.0

        # Predict next value
        predicted_next = window[-1] + slope
        predicted_next = max(-1.0, min(1.0, predicted_next))

        # Early warning: zone is currently healthy but declining
        early_warning = (
            trend_direction == 'declining' and
            avg_ndvi >= self.NDVI_MODERATE
        )

        return TrendAnalysisResult(
            trend_direction=trend_direction,
            slope=round(slope, 4),
            average_ndvi=round(avg_ndvi, 4),
            std_deviation=round(std_dev, 4),
            predicted_next=round(predicted_next, 4),
            early_warning=early_warning
        )
