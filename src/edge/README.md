# src/edge/README.md

# Edge Computing Module

Real-time edge inference and autonomous decision-making on drone hardware.

## Features

- On-device model inference with <100ms latency
- Lightweight model optimization (TensorFlow Lite, ONNX)
- Autonomous decision making without cloud connectivity
- Resource-constrained device support
- Battery-optimized processing pipeline

## Module Structure

```
edge/
├── __init__.py
├── inference/
│   ├── model_loader.py         # Load optimized models
│   ├── lightweight_inference.py # TFLite and ONNX runtime
│   └── quantization.py         # Model quantization utilities
├── processing/
│   ├── data_processor.py       # Real-time data processing
│   ├── feature_extraction.py   # Extract features for inference
│   └── post_processing.py      # Result interpretation
├── autonomous/
│   ├── decision_engine.py      # Autonomous decision logic
│   ├── action_executor.py      # Execute drone commands
│   └── safety_validator.py     # Safety checks before actions
└── resource_manager.py         # CPU, memory, and power management
```

## Supported Edge Devices

- **NVIDIA Jetson Xavier NX** - Full ML inference support
- **NVIDIA Jetson Orin Nano** - Latest-gen edge AI
- **Intel Movidius VPU** - Optimized neural network processing
- **ARM-based systems** - Lightweight inference (Cortex-A series)

## Model Optimization

- **Quantization**: 8-bit integer precision (90% smaller models)
- **Pruning**: Reduce model parameters by 70%
- **Knowledge Distillation**: 50% faster inference
- **Target Latency**: <100 ms for crop health classification

## Example Usage

```python
from edge.inference import EdgeInferenceEngine
from edge.autonomous import DecisionEngine

# Initialize edge inference
engine = EdgeInferenceEngine(model_type='crop_classifier')
engine.load_model('models/crop_classifier_lite.tflite')

# Run autonomous analysis
decision = DecisionEngine()
result = decision.analyze_and_decide(sensor_data)
```

## Testing

Run edge computing tests:
```bash
pytest tests/unit/test_edge.py -v
```

## Performance Metrics

- Model inference latency: <100 ms
- Memory footprint: <500 MB
- Power consumption: <5W (peak)
- Supported FPS: 2-5 FPS (real-time processing)
