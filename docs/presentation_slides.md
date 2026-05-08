# Unit 4 Presentation — 4 Slides Content
## 5G & Satellite-Based AI Drone System for Precision Agriculture
**Author:** Mudassir Hussain | MSIT 5910-01 Capstone | May 2026

---

## SLIDE 1 — Project Introduction

**TITLE:**
5G & Satellite-Based AI Drone System for Precision Agriculture

**SUBTITLE:**
MSIT 5910-01 Capstone | Unit 4 System Demonstration | Mudassir Hussain

---

**PURPOSE (left column):**
Traditional farming wastes up to 40% of water through uniform irrigation.
This system deploys AI-powered drones to scan every crop zone in real time
and apply water only where it is needed.

Blueprint Targets:
  ✔  35% reduction in water consumption
  ✔  15% improvement in crop yield

---

**TARGET USERS (middle column):**
  • Large-scale farm operators
  • Agricultural cooperatives
  • Remote rural farms with limited connectivity

---

**MAIN MODULES (right column):**
  1. Drone Telemetry Processor
     → GPS, battery, sensor data collection

  2. AI Crop Health Classifier
     → NDVI-based health scoring

  3. Hybrid Connectivity Manager
     → 5G primary + LEO Satellite fallback

  4. Edge Processor
     → On-site AI inference + cloud filtering

---

**SPEAKER NOTES:**
"My project solves water waste in large-scale farming using AI drones.
The system has four modules — telemetry, AI classification, hybrid connectivity,
and edge computing. Target users are farm operators in remote areas."

---
---

## SLIDE 2 — Development Environment Setup

**TITLE:**
Development Environment Setup

---

**LEFT COLUMN — Tools & Stack:**

  IDE:          VS Code with Python Extension
  Language:     Python 3.14
  Dependencies: Standard library only (no external packages)
  Config:       YAML + JSON configuration files
  Version Control: Git — branch: development

---

**MIDDLE COLUMN — Project Structure:**

  MSIT-5910-Capstone/
  ├── src/
  │   ├── drone/               ← Telemetry module
  │   ├── ai_models/           ← AI classifier
  │   ├── connectivity/        ← 5G + satellite
  │   └── edge/                ← Edge processor
  ├── config/
  │   └── system_config.yaml   ← AES-256, TLS 1.3
  ├── simulation/
  │   └── simulation_config.json
  ├── tests/
  └── demo.py                  ← Live demo entry point

---

**RIGHT COLUMN — Key Config Values:**

  system_config.yaml:
    primary:      5G
    fallback:     LEO_SATELLITE
    encryption:   AES-256
    tls:          1.3
    zero_trust:   enabled
    ai_accuracy:  90% target

  simulation_config.json:
    field:        100 hectares
    crop:         Corn
    drones:       5
    zones:        4

---

**BOTTOM — Demo Snippet (code block):**

  # Run the full system demo
  python demo.py

  # Output:
  [OK]  system_config.yaml loaded  -->  AES-256, TLS 1.3, zero-trust=ON
  [OK]  TelemetryProcessor       -- drone GPS, battery, sensor data
  [OK]  CropHealthClassifier     -- NDVI-based AI crop health analysis
  [OK]  HybridConnectivityManager -- 5G URLLC primary / LEO NTN fallback
  [OK]  EdgeProcessor            -- real-time inference + cloud filtering

---

**SPEAKER NOTES:**
"I am using VS Code with Python 3.14. The project has no external dependencies —
everything runs on the Python standard library. Configuration is managed through
YAML and JSON files. I will now show this running live."

---
---

## SLIDE 3 — Core Functionalities

**TITLE:**
Core Functionalities — Aligned with Design Specifications

---

**TOP HALF — Functionality 1: Hybrid 5G + Satellite Connectivity**
(Implements FR-02 from System Requirements)

  How it works:
  • Drone measures RSSI signal strength at each waypoint
  • If 5G RSSI > -90 dBm  →  use 5G URLLC  (latency: 8.5ms)
  • If 5G drops below threshold  →  auto-failover to LEO Satellite NTN  (latency: 35ms)
  • Per 3GPP TS 38.300 / TR 38.821 specification

  Demo output snippet:
  ┌─────────────────────────────────────────────────────────┐
  │ [5G]  DRONE-01  Zone 1  RSSI: -75 dBm  [####-]         │
  │       Latency: 8.5ms  ✔ URLLC target met               │
  │                                                         │
  │ [SAT] DRONE-02  Zone 2  *** 5G lost -- failover ***     │
  │       Latency: 35ms   ✔ NTN target met                  │
  └─────────────────────────────────────────────────────────┘

---

**BOTTOM HALF — Functionality 2: AI Crop Health Classification**
(Implements FR-03 from System Requirements — accuracy ≥ 90%)

  How it works:
  • Drone multispectral camera captures NIR and Red light bands
  • NDVI = (NIR - Red) / (NIR + Red)   range: -1.0 to +1.0
  • NDVI > 0.6  →  Healthy   (reduce irrigation 70%)
  • NDVI 0.4–0.6  →  Stress   (increase irrigation 20%)
  • NDVI 0.2–0.4  →  Severe   (immediate inspection)
  • NDVI < 0.2  →  CRITICAL  (emergency intervention)

  Demo output snippet:
  ┌─────────────────────────────────────────────────────────┐
  │ DRONE-01  Zone 1  NDVI: 0.640  [######............]     │
  │ Health: HEALTHY   Score: 0.64   Confidence: 92%         │
  │ --> Water saved! Irrigation reduced 70%                 │
  │                                                         │
  │ DRONE-04  Zone 4  NDVI: 0.110  [#....................]  │
  │ Health: CRITICAL  Score: 0.11   Confidence: 79%         │
  │ --> ALERT: Emergency irrigation triggered               │
  └─────────────────────────────────────────────────────────┘

---

**SPEAKER NOTES:**
"I will demonstrate both functionalities live. First the connectivity module —
watch DRONE-02 automatically switch from 5G to satellite when the signal drops.
Then the AI classifier — watch Zone 4 trigger a critical alert with NDVI of 0.11."

---
---

## SLIDE 4 — System Architecture & Design Principles

**TITLE:**
System Architecture & Design Principles

---

**LEFT COLUMN — 5-Layer Architecture:**

  ┌──────────────────────────────┐
  │   LAYER 5: DASHBOARD         │  Farmer alerts + heatmaps
  ├──────────────────────────────┤
  │   LAYER 4: CLOUD ANALYTICS   │  Model retraining + storage
  ├──────────────────────────────┤
  │   LAYER 3: EDGE COMPUTING    │  On-site AI inference
  ├──────────────────────────────┤
  │   LAYER 2: CONNECTIVITY      │  5G URLLC + LEO NTN
  ├──────────────────────────────┤
  │   LAYER 1: DRONE             │  Sensors + telemetry
  └──────────────────────────────┘

---

**MIDDLE COLUMN — Design Principles Applied:**

  1. Separation of Concerns
     Each module has one job.
     TelemetryProcessor does not know about AI.
     CropHealthClassifier does not know about connectivity.
     → Makes each module independently testable.

  2. Fail-Safe Design
     5G fails → satellite takes over automatically.
     No manual intervention required.
     → 99.9% availability target (NFR-03).

  3. Edge-First Processing
     AI runs on-site, not in the cloud.
     Only alerts and summaries go to cloud.
     → 70% cloud bandwidth reduction.

  4. Modular Scalability
     TelemetryProcessor is instantiated per drone.
     Adding drone 51 = one new instance.
     → Supports 50 simultaneous drones (FR-07).

---

**RIGHT COLUMN — Architecture → Code Mapping:**

  Architecture Layer     Python Module
  ─────────────────────────────────────
  Drone Layer        →   telemetry_processor.py
  Connectivity Layer →   hybrid_connectivity_manager.py
  Edge Layer         →   edge_processor.py
  AI / Cloud Layer   →   crop_health_classifier.py
  Dashboard Layer    →   (Unit 5 — in progress)

  Post-Mission Field Heatmap:
  ┌──────────────┬──────────────┐
  │ Zone 1       │ Zone 2       │
  │ HEALTHY      │ STRESS       │
  ├──────────────┼──────────────┤
  │ Zone 3       │ Zone 4       │
  │ SEVERE       │ CRITICAL     │
  └──────────────┴──────────────┘

---

**SPEAKER NOTES:**
"The five-layer architecture directly maps to the four Python modules.
Separation of concerns means each module is independently testable —
the unit tests in the tests/ folder confirm this.
The edge-first design is what achieves the 70% bandwidth reduction you saw in the demo."

---

## HOW TO BUILD IN POWERPOINT — Quick Guide

1. Open PowerPoint → New Presentation
2. Choose a dark or professional theme (dark blue works well for tech)
3. Create 4 slides — one per section above
4. For each slide:
   - Paste the TITLE as the slide title
   - Use text boxes for columns
   - Use a dark background box (black or dark grey) for code/demo snippets
   - Use white or light text inside code boxes
   - Use green for HEALTHY, yellow for STRESS, red for CRITICAL labels
5. Font suggestions:
   - Titles: Calibri Bold 36pt
   - Body text: Calibri 18pt
   - Code snippets: Courier New 14pt in a dark box
6. Add your name + course code in the footer of every slide
