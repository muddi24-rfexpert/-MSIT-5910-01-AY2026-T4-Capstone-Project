# src/drone/README.md

# Drone Module

Drone telemetry processing, sensor data collection, and flight control integration.

## Features

- Real-time GPS and IMU data processing
- Multispectral sensor data collection (RGB, NIR, NDVI)
- Flight telemetry logging and monitoring
- Waypoint navigation and autonomous flight
- Sensor fusion and data calibration

## Module Structure

```
drone/
├── __init__.py
├── sensors/
│   ├── gps_handler.py          # GPS data processing
│   ├── imu_handler.py          # IMU and orientation
│   └── multispectral_camera.py # Multispectral sensor interface
├── telemetry.py                # Telemetry collection and logging
├── flight_control.py           # Flight command interface
└── data_logger.py              # Data persistence and timestamping
```

## Supported Drones

- DJI Matrice 300 RTK
- DJI Phantom 4 Pro V2.0
- Custom drone with ArduCopter firmware

## Sensor Data

The drone module collects:
- **GPS**: Latitude, Longitude, Altitude, Accuracy
- **IMU**: Pitch, Roll, Yaw, Acceleration (X, Y, Z)
- **Camera**: RGB images, Multispectral bands (Red, Green, Blue, Red Edge, NIR)
- **Battery**: Voltage, Current, Temperature, Remaining %

## Example Usage

```python
from drone.telemetry import TelemetryCollector
from drone.sensors import MultispectralCamera

telemetry = TelemetryCollector()
camera = MultispectralCamera()

# Start collecting data
telemetry.start()
images = camera.capture_multispectral_frame()
```

## Testing

Run drone module tests:
```bash
pytest tests/unit/test_drone.py -v
```
