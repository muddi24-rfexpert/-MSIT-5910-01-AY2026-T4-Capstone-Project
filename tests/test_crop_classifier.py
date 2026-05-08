"""
Unit Tests — Crop Health Classifier
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 2.0 | Date: May 8, 2026

Testing approach: White-box testing — tests are designed with knowledge
of internal NDVI thresholds, classification logic, and trend analysis algorithm.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_models.crop_health_classifier import CropHealthClassifier, TrendAnalysisResult


class TestNDVICalculation:
    """White-box tests for NDVI calculation algorithm."""

    def setup_method(self):
        self.clf = CropHealthClassifier()

    def test_ndvi_healthy_vegetation(self):
        """High NIR, low Red = healthy vegetation (NDVI > 0.6)."""
        ndvi = self.clf.calculate_ndvi(nir_band=0.8, red_band=0.2)
        assert ndvi == pytest.approx(0.6, abs=0.01)
        print(f"PASS: Healthy vegetation NDVI = {ndvi:.3f}")

    def test_ndvi_bare_soil(self):
        """Similar NIR and Red = bare soil (NDVI near 0)."""
        ndvi = self.clf.calculate_ndvi(nir_band=0.3, red_band=0.3)
        assert ndvi == pytest.approx(0.0, abs=0.01)
        print(f"PASS: Bare soil NDVI = {ndvi:.3f}")

    def test_ndvi_water_body(self):
        """Low NIR, high Red = water body (negative NDVI)."""
        ndvi = self.clf.calculate_ndvi(nir_band=0.1, red_band=0.5)
        assert ndvi < 0
        print(f"PASS: Water body NDVI = {ndvi:.3f}")

    def test_ndvi_division_by_zero(self):
        """Both bands zero should not crash (edge case)."""
        ndvi = self.clf.calculate_ndvi(nir_band=0.0, red_band=0.0)
        assert -1.0 <= ndvi <= 1.0
        print(f"PASS: Zero division handled, NDVI = {ndvi:.3f}")

    def test_ndvi_clamping(self):
        """NDVI should always be between -1.0 and 1.0."""
        ndvi_max = self.clf.calculate_ndvi(nir_band=1.0, red_band=0.0)
        ndvi_min = self.clf.calculate_ndvi(nir_band=0.0, red_band=1.0)
        assert ndvi_max <= 1.0
        assert ndvi_min >= -1.0
        print(f"PASS: Clamping works — max={ndvi_max:.3f}, min={ndvi_min:.3f}")

    def test_ndvi_ordering(self):
        """Higher NIR/Red ratio should produce higher NDVI."""
        ndvi_high = self.clf.calculate_ndvi(0.8, 0.2)
        ndvi_mid = self.clf.calculate_ndvi(0.6, 0.3)
        ndvi_low = self.clf.calculate_ndvi(0.4, 0.5)
        assert ndvi_high > ndvi_mid > ndvi_low
        print(f"PASS: NDVI ordering correct — {ndvi_high:.3f} > {ndvi_mid:.3f} > {ndvi_low:.3f}")


class TestHealthClassification:
    """White-box tests for crop health classification logic."""

    def setup_method(self):
        self.clf = CropHealthClassifier()

    def test_healthy_crop(self):
        """NDVI >= 0.6 should classify as healthy."""
        result = self.clf.classify_health(ndvi_value=0.75)
        assert result.stress_detected is False
        assert result.stress_type == 'none'
        assert result.health_score >= 0.6
        assert result.confidence == 0.92
        print(f"PASS: Healthy crop — NDVI={result.ndvi_value}, Score={result.health_score}")

    def test_moderate_stress_nutrient(self):
        """NDVI 0.4-0.6 without high thermal = nutrient stress."""
        result = self.clf.classify_health(ndvi_value=0.50, thermal_value=30.0)
        assert result.stress_detected is True
        assert result.stress_type == 'nutrient'
        assert result.confidence == 0.87
        print(f"PASS: Nutrient stress — NDVI={result.ndvi_value}, Type={result.stress_type}")

    def test_moderate_stress_water(self):
        """NDVI 0.4-0.6 with high thermal (>35C) = water stress."""
        result = self.clf.classify_health(ndvi_value=0.50, thermal_value=38.0)
        assert result.stress_detected is True
        assert result.stress_type == 'water'
        print(f"PASS: Water stress — NDVI={result.ndvi_value}, Thermal=38C")

    def test_significant_stress(self):
        """NDVI 0.2-0.4 should classify as disease stress."""
        result = self.clf.classify_health(ndvi_value=0.25)
        assert result.stress_detected is True
        assert result.stress_type == 'disease'
        assert result.health_score < 0.4
        print(f"PASS: Disease stress — NDVI={result.ndvi_value}, Type={result.stress_type}")

    def test_critical_crop(self):
        """NDVI < 0.2 should classify as critical with emergency recommendation."""
        result = self.clf.classify_health(ndvi_value=0.10)
        assert result.stress_detected is True
        assert result.stress_type == 'pest'
        assert 'CRITICAL' in result.recommendation
        print(f"PASS: Critical crop — NDVI={result.ndvi_value}, Rec={result.recommendation[:40]}...")

    def test_boundary_healthy(self):
        """NDVI exactly at 0.6 threshold should be healthy."""
        result = self.clf.classify_health(ndvi_value=0.6)
        assert result.stress_detected is False
        print(f"PASS: Boundary test — NDVI=0.6 classified as healthy")


class TestTrendAnalysis:
    """White-box tests for time-series trend analysis algorithm."""

    def setup_method(self):
        self.clf = CropHealthClassifier()

    def test_insufficient_data(self):
        """Should return None with fewer than TREND_WINDOW_SIZE readings."""
        self.clf.record_ndvi("zone-1", 0.7)
        self.clf.record_ndvi("zone-1", 0.68)
        result = self.clf.analyze_trend("zone-1")
        assert result is None
        print("PASS: Insufficient data returns None")

    def test_declining_trend(self):
        """Consistently decreasing NDVI should detect declining trend."""
        for val in [0.8, 0.75, 0.70, 0.65, 0.60]:
            self.clf.record_ndvi("zone-decline", val)
        result = self.clf.analyze_trend("zone-decline")
        assert result is not None
        assert result.trend_direction == 'declining'
        assert result.slope < 0
        print(f"PASS: Declining trend detected — slope={result.slope}")

    def test_improving_trend(self):
        """Consistently increasing NDVI should detect improving trend."""
        for val in [0.3, 0.38, 0.45, 0.52, 0.60]:
            self.clf.record_ndvi("zone-improve", val)
        result = self.clf.analyze_trend("zone-improve")
        assert result is not None
        assert result.trend_direction == 'improving'
        assert result.slope > 0
        print(f"PASS: Improving trend detected — slope={result.slope}")

    def test_stable_trend(self):
        """Flat NDVI readings should detect stable trend."""
        for val in [0.65, 0.66, 0.64, 0.65, 0.65]:
            self.clf.record_ndvi("zone-stable", val)
        result = self.clf.analyze_trend("zone-stable")
        assert result is not None
        assert result.trend_direction == 'stable'
        print(f"PASS: Stable trend detected — slope={result.slope}")

    def test_early_warning(self):
        """Declining trend in healthy zone should trigger early warning."""
        for val in [0.80, 0.75, 0.70, 0.65, 0.60]:
            self.clf.record_ndvi("zone-warning", val)
        result = self.clf.analyze_trend("zone-warning")
        assert result is not None
        assert result.early_warning is True
        print(f"PASS: Early warning triggered — avg_ndvi={result.average_ndvi}")

    def test_no_early_warning_low_ndvi(self):
        """Declining trend in already-stressed zone should NOT trigger early warning."""
        for val in [0.35, 0.32, 0.28, 0.25, 0.22]:
            self.clf.record_ndvi("zone-already-stressed", val)
        result = self.clf.analyze_trend("zone-already-stressed")
        assert result is not None
        assert result.early_warning is False
        print(f"PASS: No early warning for already-stressed zone")

    def test_prediction(self):
        """Predicted next value should follow the trend."""
        for val in [0.5, 0.55, 0.60, 0.65, 0.70]:
            self.clf.record_ndvi("zone-predict", val)
        result = self.clf.analyze_trend("zone-predict")
        assert result is not None
        assert result.predicted_next > 0.70  # Should predict higher
        print(f"PASS: Prediction = {result.predicted_next} (above last reading 0.70)")

    def test_unknown_zone(self):
        """Unknown zone should return None."""
        result = self.clf.analyze_trend("nonexistent-zone")
        assert result is None
        print("PASS: Unknown zone returns None")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
