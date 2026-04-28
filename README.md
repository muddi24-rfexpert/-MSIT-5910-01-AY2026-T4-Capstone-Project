# 5G and Satellite-Based AI Drone System for Precision Agriculture

## Project Overview

This capstone project focuses on developing an **Integrated AI-Powered Drone System** that leverages **5G** and **Non-Terrestrial Networks (NTN) - Satellite** connectivity for precision agriculture. The system combines real-time drone telemetry, edge computing, machine learning models, and satellite-based communication to enable autonomous crop monitoring, health analysis, and yield prediction in remote agricultural regions.

## Key Features

- **Autonomous Drone Operations**: Real-time telemetry processing and flight control
- **AI-Powered Crop Analysis**: Machine learning models for crop health assessment and anomaly detection
- **5G/Satellite Connectivity**: Hybrid communication system for continuous connectivity in remote areas
- **Edge Computing**: On-drone processing for real-time decision making with minimal latency
- **Data Analytics**: Comprehensive simulation and performance benchmarking

## Project Structure

```
ai-5g-ntn-drone-agriculture/
│
├── src/                    # Core source code modules
│   ├── drone/              # Drone telemetry and sensor processing
│   ├── ai_models/          # Machine learning models for crop analysis
│   ├── connectivity/       # 5G and satellite communication modules
│   └── edge/               # Edge computing and real-time processing
│
├── docs/                   # Project documentation (SRS, reports)
├── design/                 # Architecture and workflow diagrams
├── simulation/             # Datasets and simulation outputs
├── config/                 # Configuration files
├── tests/                  # Unit and integration test scripts
│
├── README.md               # Project overview and usage
└── requirements.txt        # Dependencies
```

## Branching Strategy & Version Control

### Branch Hierarchy

```
main (Stable & Production-Ready)
  │
  └── development (Integration Branch)
       ├── feature/ai-model (AI Model Development)
       ├── feature/satellite (Satellite Connectivity)
       └── bugfix/edge-processing (Edge Computing Fixes)
```

### Branch Descriptions

| Branch | Purpose | Status |
|--------|---------|--------|
| **main** | Stable, production-ready version | Active |
| **development** | Integration of all active features | Active |
| **feature/ai-model** | AI/ML model development and optimization | Active |
| **feature/satellite** | Satellite connectivity implementation | Active |
| **bugfix/edge-processing** | Edge computing fixes and optimization | Active |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/muddi24-rfexpert/-MSIT-5910-01-AY2026-T4-Capstone-Project.git
cd -MSIT-5910-01-AY2026-T4-Capstone-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Repository URL

**GitHub Repository**: https://github.com/muddi24-rfexpert/-MSIT-5910-01-AY2026-T4-Capstone-Project

**Access Level**: Private Repository (Contributor permissions)

## Commit Message Conventions

All commits follow a structured format to ensure clear documentation:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples:

- `feat(drone): implement telemetry data collection from flight sensors`
- `feat(ai-models): add CNN for crop disease detection`
- `feat(connectivity): establish 5G communication protocol`
- `fix(edge): optimize real-time processing latency`
- `docs: update API documentation and system architecture`
- `test: add unit tests for drone sensor processing`

## Version Control for Documentation & Traceability

### Key Practices:

1. **Atomic Commits**: Each commit represents a single logical change for easy rollback
2. **Descriptive Messages**: All commits include detailed messages linking to issues/features
3. **Branch Protection**: Main branch requires PR reviews before merging
4. **Pull Request Documentation**: Each PR includes:
   - Detailed description of changes
   - Link to related issues
   - Testing methodology
   - Performance impact analysis

5. **Documentation Synchronization**:
   - Architecture diagrams updated with code changes
   - API documentation maintained in `/docs`
   - SRS versioned alongside code releases
   - Change logs maintained for each release

6. **Traceability**:
   - All commits linked to specific modules (drone, ai_models, connectivity, edge)
   - Issues tracked and referenced in commits
   - Version tags applied to production releases
   - Audit trail maintained for compliance

## Team Collaboration

- **Pull Request Reviews**: Minimum 1 approval required before merging to development
- **Continuous Integration**: Automated tests run on all PRs
- **Code Quality**: Linting and formatting standards enforced
- **Release Management**: Scheduled releases from development → main with semantic versioning

## Getting Started

1. Create a feature branch from `development`
2. Make your changes with clear, descriptive commits
3. Create a Pull Request to development branch
4. Await code review and approval
5. Merge and delete feature branch

## Contact & Support

For questions or issues, please create a GitHub Issue in the repository.

---

**Last Updated**: April 28, 2026  
**Project Lead**: muddi24-rfexpert  
**Status**: Active Development
