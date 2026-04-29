"""
Unit Tests — Crop Health Classifier
5G and Satellite-Based AI Drone System for Precision Agriculture
Author: Mudassir Hussain
Version: 1.0 | Date: April 28, 2026
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_models.crop_health_classifier import CropHealthClassifier


def test_healthy_crop():
    clf = CropHealthClassifier()
    result = clf.classify_health(ndvi_value=0.75)
    assert result.stress_detected == False
    assert result.stress_type == 'none'
    assert result.health_score >= 0.6
    print(f"PASS: Healthy crop — NDVI={result.ndvi_value}, Score={result.health_score}")


def test_stressed_crop():
    clf = CropHealthClassifier()
    result = clf.classify_health(ndvi_value=0.25)
    assert result.stress_detected == True
    assert result.health_score < 0.4
    print(f"PASS: Stressed crop — NDVI={result.ndvi_value}, Type={result.stress_type}")


def test_critical_crop():
    clf = CropHealthClassifier()
    result = clf.classify_health(ndvi_value=0.10)
    assert result.stress_detected == True
    assert 'CRITICAL' in result.recommendation
    print(f"PASS: Critical crop — NDVI={result.ndvi_value}, Recommendation={result.recommendation[:40]}...")


def test_ndvi_calculation():
    import numpy as np
    clf = CropHealthClassifier()
    nir = np.array([0.8, 0.6, 0.4])
    red = np.array([0.2, 0.3, 0.5])
    ndvi = clf.calculate_ndvi(nir, red)
    assert ndvi[0] > ndvi[1] > ndvi[2]
    print(f"PASS: NDVI calculation — values={ndvi}")


if __name__ == '__main__':
    print("Running Unit Tests — Crop Health Classifier")
    print("=" * 50)
    test_healthy_crop()
    test_stressed_crop()
    test_critical_crop()
    test_ndvi_calculation()
    print("=" * 50)
    print("All tests passed!")
