# 5G and Satellite-Based AI Drone System for Precision Agriculture

## Project Overview

**AgriDrone-5G-NTN** is a capstone project implementing an integrated AI-powered drone system that leverages **5G URLLC** and **LEO Satellite NTN** connectivity for precision agriculture. The system combines real-time drone telemetry, edge computing, AI crop health classification, and hybrid connectivity to enable autonomous crop monitoring and automated irrigation decisions in rural environments.

**Author:** Mudassir Hussain | **Course:** MSIT 5910-01 Capstone | **University of the People**

## Key Achievements

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Pipeline Latency | 0.061 ms | < 10 ms | PASS |
| Throughput | ~29,000 r/s | >= 50 r/s | PASS |
| AI Accuracy | 100% | >= 90% | PASS |
| Edge Bandwidth Reduction | 70% | >= 70% | PASS |
| Memory Footprint | 0.14 MB | < 512 MB | PASS |
| Unit Tests | 96 passing | All pass | PASS |

## System Architecture

```
+------------------------------------------+
|       FARMER DASHBOARD LAYER             |
|   Web/Mobile UI - Heatmaps - Alerts      |
+--------------------+---------------------+
                     |
+--------------------v---------------------+
|       CLOUD ANALYTICS LAYER              |
|   Model Training - Long-term Storage     |
+--------------------+---------------------+
                     |
+--------------------v---------------------+
|       EDGE COMPUTING LAYER               |
|   Real-time AI Inference - Filtering     |
+--------------------+---------------------+
                     |
+--------------------v---------------------+
|    HYBRID CONNECTIVITY LAYER             |
|   5G gNB (Primary) <-> LEO NTN (Fallback)|
+--------------------+---------------------+
                     |
+--------------------v---------------------+
|         DRONE LAYER                      |
|  Multispectral - LiDAR - GPS - Thermal   |
+------------------------------------------+
```

## Core Modules

| Module | Description | Version |
|--------|-------------|---------|
| `crop_health_classifier.py` | NDVI classification + time-series trend analysis | v2.0 |
| `hybrid_connectivity_manager.py` | 5G/Satellite failover + timing advance + Doppler | v2.0 |
| `telemetry_processor.py` | Drone data processing + GPS path optimization | v2.0 |
| `edge_processor.py` | Intelligent filtering + model updates + rollback | v2.0 |
| `system_integration.py` | Unified pipeline orchestrating all modules | v3.0 |

## Quick Start

```bash
# Clone
git clone https://github.com/muddi24-rfexpert/-MSIT-5910-01-AY2026-T4-Capstone-Project.git
cd -MSIT-5910-01-AY2026-T4-Capstone-Project

# Install
pip install -r requirements.txt

# Run tests (96 tests)
python -m pytest tests/ -v

# Run performance benchmarks
python tests/performance_benchmark.py

# Run system integration demo
python src/system_integration.py

# Run full interactive demo
python demo.py
```

## Project Structure

```
MSIT-5910-Capstone/
├── src/
│   ├── ai_models/crop_health_classifier.py
│   ├── connectivity/hybrid_connectivity_manager.py
│   ├── drone/telemetry_processor.py
│   ├── edge/edge_processor.py
│   └── system_integration.py
├── tests/
│   ├── test_crop_classifier.py (20 tests)
│   ├── test_connectivity_manager.py (20 tests)
│   ├── test_telemetry_processor.py (18 tests)
│   ├── test_edge_processor.py (19 tests)
│   ├── test_system_integration.py (19 tests)
│   └── performance_benchmark.py (5 benchmarks)
├── config/system_config.yaml
├── docs/
├── demo.py
├── requirements.txt
└── README.md
```

## Version History

| Tag | Milestone | Date |
|-----|-----------|------|
| v1.0 | Initial Development (Units 1-4) | May 2026 |
| v2.0 | Core Logic & Testing (Unit 5) | May 2026 |
| v3.0 | System Integration & Performance (Unit 6) | May 2026 |
| v4.0 | Comprehensive Testing (Unit 7) | May 2026 |
| v5.0-final | Final Capstone Submission (Unit 8) | May 2026 |

## Branching Strategy

- **main**: Stable, production-ready releases
- **development**: Active development and integration

## Technologies

- Python 3.14 | PyTest 9.0.3 | Git/GitHub
- 3GPP TS 38.300 (5G NR) | 3GPP TR 38.821 (NTN)
- AES-256 + TLS 1.3 | Zero-Trust Architecture

---
**Repository:** https://github.com/muddi24-rfexpert/-MSIT-5910-01-AY2026-T4-Capstone-Project  
**Last Updated:** May 2026 | **Status:** Complete
