# src/connectivity/README.md

# Connectivity Module

5G and Non-Terrestrial Networks (NTN) satellite communication integration.

## Features

- 5G cellular connectivity with dual-band support
- Satellite communication fallback (LEO/GEO)
- Network switching and failover management
- QoS monitoring and adaptive bitrate streaming
- Low-latency data transmission optimization

## Module Structure

```
connectivity/
├── __init__.py
├── 5g/
│   ├── modem_interface.py      # 5G modem control
│   ├── network_config.py       # Network configuration
│   └── signal_monitor.py       # Signal strength monitoring
├── satellite/
│   ├── ntn_handler.py          # Satellite communication
│   ├── ephemeris_manager.py    # Satellite tracking
│   └── handover.py             # Network handover logic
├── network_manager.py          # Network selection and switching
└── performance_monitor.py      # QoS and latency metrics
```

## 5G Connectivity

- **Frequency Bands**: n78 (3.5 GHz), n79 (4.7 GHz)
- **Target Throughput**: ≥100 Mbps
- **Latency**: <50 ms
- **Coverage**: Urban and suburban areas

## Satellite Connectivity

- **LEO Constellation**: Starlink, OneWeb
- **GEO Options**: Inmarsat, Intelsat
- **Latency**: 200-600 ms (LEO), 600-800 ms (GEO)
- **Fallback Mode**: Automatic when 5G unavailable

## Example Usage

```python
from connectivity.network_manager import NetworkManager

nm = NetworkManager()
nm.connect()  # Auto-select best network

# Monitor connection quality
stats = nm.get_connection_stats()
print(f"Latency: {stats.latency}ms")
print(f"Throughput: {stats.throughput}Mbps")
```

## Testing

Run connectivity tests:
```bash
pytest tests/unit/test_connectivity.py -v
```
