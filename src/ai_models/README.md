# src/ai_models/README.md

# AI Models Module

Machine learning models for crop analysis, disease detection, and yield prediction.

## Features

- Crop health classification (healthy/diseased/stress)
- Disease identification and severity assessment
- Yield prediction using multispectral data
- NDVI (Normalized Difference Vegetation Index) calculation
- Model training and evaluation pipelines

## Module Structure

```
ai_models/
├── __init__.py
├── models/
│   ├── cnn_crop_classifier.py    # CNN for crop health
│   ├── disease_detector.py        # Disease detection model
│   └── yield_predictor.py         # Yield prediction model
├── preprocessing.py               # Image and data preprocessing
├── inference.py                   # Real-time inference pipeline
└── training.py                    # Model training utilities
```

## Dependencies

- tensorflow>=2.8.0
- torch>=1.10.0
- scikit-learn>=1.0.0
- PIL>=8.0.0

## Pre-trained Models

Pre-trained models are stored in `/models/checkpoints/`:
- `crop_classifier_v1.h5` - Crop health classification
- `disease_detector_v1.pt` - Disease detection
- `yield_predictor_v1.h5` - Yield prediction

## Example Usage

```python
from ai_models.inference import CropAnalyzer

analyzer = CropAnalyzer(model_path='models/checkpoints/crop_classifier_v1.h5')
results = analyzer.analyze_image('image.jpg')
```

## Testing

Run AI models tests:
```bash
pytest tests/unit/test_ai_models.py -v
```
