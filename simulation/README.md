# simulation/README.md

# Simulation Environment & Datasets

This directory contains simulation scripts, test data, and performance benchmarking outputs.

## Directory Structure

```
simulation/
├── datasets/
│   ├── crop_images/           # Sample crop images for testing
│   ├── sensor_data/           # Simulated sensor telemetry
│   └── satellite_data/        # Simulated satellite imagery
├── scenarios/
│   ├── agricultural_field_1.json
│   ├── agricultural_field_2.json
│   └── remote_area_coverage.json
├── outputs/
│   ├── performance_logs/      # Simulation performance metrics
│   ├── results/               # Simulation results and analysis
│   └── reports/               # Generated reports
└── scripts/
    ├── simulate_drone_flight.py
    ├── simulate_connectivity.py
    └── simulate_inference.py
```

## Running Simulations

```bash
# Run full end-to-end simulation
python simulation/scripts/simulate_drone_flight.py

# Run connectivity simulation
python simulation/scripts/simulate_connectivity.py

# Run inference simulation
python simulation/scripts/simulate_inference.py
```

## Benchmark Results

Simulation outputs and performance benchmarks are stored in the `outputs/` directory.

## Adding New Datasets

1. Place raw data in appropriate `datasets/` subdirectory
2. Create preprocessing script if needed
3. Update documentation with data description
