# Unit 4 — System Demonstration Video Script
## 5G & Satellite-Based AI Drone System for Precision Agriculture
**Author:** Mudassir Hussain | **Course:** MSIT 5910-01 | **Duration:** 5–7 minutes
**Tool:** ScreenPal | **IDE:** VS Code (standalone)

---

## BEFORE YOU HIT RECORD — Setup Checklist

- [ ] Open plain VS Code (no Kiro) with the project folder
- [ ] Open terminal inside VS Code (Ctrl + `)
- [ ] Have `demo.py` visible in the Explorer sidebar
- [ ] Font size bumped up: Ctrl + = (so text is readable on recording)
- [ ] ScreenPal set to record full screen + webcam bubble
- [ ] Government ID ready in hand

---

## ── SEGMENT 1 — ID Verification (0:00 – 0:30) ──────────────────────────────

> Face the webcam. Hold your ID clearly in frame.

"Hi, my name is Mudassir Hussain. I am enrolled in MSIT 5910-01, Capstone Project.
Here is my government-issued photo ID."

*(Hold ID steady and readable for 5–10 seconds)*

"Thank you. Let me now walk you through my Unit 4 system demonstration."

---

## ── SEGMENT 2 — Project Introduction (0:30 – 1:45) ─────────────────────────

> Stay on webcam or switch to VS Code with README.md open.

"My capstone project is titled:
**5G and Satellite-Based AI Drone System for Precision Agriculture.**

**Purpose:**
The problem I am solving is inefficient water usage and low crop yields
in large-scale farming. Traditional irrigation applies water uniformly
across an entire field — wasting up to 40% of water on healthy crops
that do not need it.

My system deploys AI-powered drones that scan every crop zone in real time,
classify the health of each zone using machine learning, and apply
precision irrigation only where it is actually needed.

The blueprint targets are:
- 35% reduction in water consumption
- 15% improvement in crop yield

**Target Users:**
Large-scale farm operators and agricultural cooperatives —
especially in remote rural areas where internet connectivity is unreliable.

**Main Modules — there are four:**

*(Click through each folder in the VS Code Explorer as you name them)*

- Module 1 — Drone telemetry processor:
  collects GPS, battery, and sensor readings from the drone in flight

- Module 2 — AI Crop Health Classifier:
  analyses multispectral camera data using NDVI to score crop health

- Module 3 — Hybrid Connectivity Manager:
  switches automatically between 5G and LEO satellite when signal drops

- Module 4 — Edge Processor:
  runs AI inference on-site, filters routine data, only sends alerts to cloud"

---

## ── SEGMENT 3 — Development Environment Setup (1:45 – 3:15) ────────────────

> Show VS Code Explorer. Open terminal with Ctrl + `

"Let me show you the development environment setup.

I am using **VS Code** as my IDE with the Python extension installed.
The language is **Python 3.11**.

*(Show the folder structure in the Explorer sidebar)*

The project is organised into four source modules under the `src/` directory —
drone, ai_models, connectivity, and edge — each one maps directly to a layer
in our five-layer system architecture.

*(Open `config/system_config.yaml` in the editor)*

Configuration is managed through `system_config.yaml`.
You can see the key settings here:
- Primary connectivity: 5G, fallback: LEO Satellite
- Encryption: AES-256 with TLS 1.3
- Zero-trust security: enabled
- AI model accuracy target: 90%

*(Open `simulation/simulation_config.json`)*

And `simulation_config.json` defines the field parameters —
100 hectares, 5 drones, 4 irrigation zones, corn crop type.
These values drive the simulation you are about to see.

*(Switch to terminal — Ctrl + `)*

The only external dependency is NumPy for the NDVI matrix calculations.
I install it with:"

```
pip install -r requirements.txt
```

*(Run it — show it completing successfully)*

"Installation complete. The environment is ready.
Now let me run the system."

---

## ── SEGMENT 4 — Core Functionality 1: Hybrid 5G + Satellite Connectivity (3:15 – 4:45) ──

> Terminal is open. Type: python demo.py — press ENTER

```
python demo.py
```

*(Press ENTER at the first pause — Module 1 initialises)*

"The system is initialising all four modules.
You can see each one loading successfully —
TelemetryProcessor, CropHealthClassifier, HybridConnectivityManager, EdgeProcessor.

It also confirms the pre-flight AI analysis:
satellite imagery processed, weather loaded, optimised flight path generated
for 5 drones across the 100-hectare field.

*(Press ENTER at the second pause — Module 2: Connectivity runs)*

This is **Core Functionality 1 — Hybrid Connectivity.**

This directly implements Functional Requirement FR-02 from our SRS:
'System shall support hybrid communication using 5G NR with automatic
LEO satellite NTN failover.'

Watch what happens drone by drone:

*(Point to DRONE-01)*
DRONE-01 in Zone 1 — strong 5G signal at minus 75 dBm.
Mode: 5G. Latency: 8.5 milliseconds. Our URLLC target is under 10ms — met.

*(Point to DRONE-02 failover line)*
DRONE-02 in Zone 2 — the 5G signal weakens and drops below minus 90 dBm threshold.
The system automatically switches to LEO Satellite NTN.
Latency: 35 milliseconds. Our NTN target is under 50ms — met.

*(Point to DRONE-03 and DRONE-04)*
Zones 3 and 4 are deep rural — satellite only.
Still within the 50ms target.

This is the 3GPP Release 17 NTN specification for non-terrestrial network handover
implemented in our HybridConnectivityManager module."

---

## ── SEGMENT 5 — Core Functionality 2: AI Crop Health Classification (4:45 – 6:15) ──

*(Press ENTER at the third pause — Module 3: AI Classification runs)*

"This is **Core Functionality 2 — AI Crop Health Classification.**

This implements Functional Requirement FR-03:
'System shall process crop health data using ML models with accuracy of 90% or greater.'

The drone's multispectral camera captures two bands of light —
Near-Infrared and Red. The system calculates NDVI using the formula:

  NDVI = (NIR minus Red) divided by (NIR plus Red)

NDVI ranges from minus 1 to plus 1.
Above 0.6 is healthy. Below 0.2 is critical.

*(Point to Zone 1 — green output)*
Zone 1: NDVI 0.82 — healthy crop. No stress detected. Confidence 92%.
Recommendation: standard monitoring. Irrigation reduced by 70% here.
That is exactly how we achieve the 35% water saving.

*(Point to Zone 2 — yellow output)*
Zone 2: NDVI 0.52 — moderate stress, water stress detected.
System recommends increasing irrigation by 20%.

*(Point to Zone 4 — red CRITICAL output)*
Zone 4: NDVI 0.11 — CRITICAL. Severe crop stress.
The system raises an emergency alert and triggers immediate irrigation.
This reading is flagged for cloud upload.

Notice the Cloud Upload column —
healthy routine readings say 'NO — filtered at edge.'
Only alerts go to the cloud. That is our edge computing layer
reducing cloud bandwidth by 70%."

---

## ── SEGMENT 6 — Architecture & Design Principles (6:15 – 7:00) ─────────────

*(Press ENTER at the fourth pause — Modules 4 & 5: Edge stats + Scorecard)*

"The edge computing summary confirms:
9 readings processed locally, cloud transmissions reduced significantly —
hitting our 70% bandwidth reduction target.

The final scorecard validates every blueprint target:

*(Read through the scorecard on screen)*
- Water reduction — achieved
- Yield improvement — on track
- 5G latency 8.5ms — target met
- Satellite latency 35ms — target met
- AI confidence 87 to 92% — at our 90% target
- AES-256 encryption and zero-trust — configured

**How architecture guided implementation:**

Our five-layer architecture — Drone, Connectivity, Edge, Cloud, Dashboard —
maps directly to the four Python modules you saw.
Each module has one responsibility. They do not depend on each other directly.
This separation of concerns means I can test each module independently,
which is why the unit tests in the `tests/` folder run cleanly.

It also means the system scales — FR-07 requires support for 50 simultaneous drones.
Because TelemetryProcessor is instantiated per drone, scaling is just
adding more instances. No architectural change needed."

---

## ── SEGMENT 7 — Closing (7:00 – 7:30) ──────────────────────────────────────

"To summarise what I demonstrated today:

1. Project introduction — purpose, target users, and four main modules
2. Development environment — VS Code, Python 3.11, NumPy, YAML and JSON config
3. Core Functionality 1 — Hybrid 5G and satellite connectivity with automatic failover
4. Core Functionality 2 — AI crop health classification using NDVI analysis
5. Architecture validation — all five layers active, all blueprint targets met

The system is in active Unit 4 development.
Next steps are CNN model training with real crop imagery
and building the farmer dashboard prototype.

Thank you."

---

## Timing Guide

| Segment | Content | Time |
|---------|---------|------|
| 1 | ID Verification | 0:00 – 0:30 |
| 2 | Project Introduction | 0:30 – 1:45 |
| 3 | Dev Environment Setup | 1:45 – 3:15 |
| 4 | Core Functionality 1 — Connectivity | 3:15 – 4:45 |
| 5 | Core Functionality 2 — AI Classification | 4:45 – 6:15 |
| 6 | Architecture & Design Principles | 6:15 – 7:00 |
| 7 | Closing | 7:00 – 7:30 |

**Total: ~7:30** — trim pauses between ENTER presses to land at exactly 7 minutes.

---

## What to have open in VS Code before recording

| Step | What to show |
|------|-------------|
| Segment 2 | Explorer sidebar — folder tree visible |
| Segment 3 | `config/system_config.yaml` open in editor |
| Segment 3 | `simulation/simulation_config.json` open in editor |
| Segment 3 | Terminal — run `pip install -r requirements.txt` |
| Segments 4–6 | Terminal — run `python demo.py`, press ENTER 4 times |

---

## Rubric Checklist

| Rubric Requirement | Covered In |
|---|---|
| Brief introduction — purpose, target users, main modules | Segment 2 |
| Development environment setup — IDE, frameworks, dependencies | Segment 3 |
| Core functionality 1 aligned with design specs | Segment 4 |
| Core functionality 2 aligned with design specs | Segment 5 |
| How architecture/design principles guided implementation | Segment 6 |
