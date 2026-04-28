# tests/README.md

# Testing Framework

This directory contains all unit, integration, and system tests for the capstone project.

## Test Structure

```
tests/
├── unit/              # Unit tests for individual modules
│   ├── test_drone.py
│   ├── test_ai_models.py
│   ├── test_connectivity.py
│   └── test_edge.py
├── integration/       # Integration tests between modules
│   ├── test_drone_connectivity.py
│   ├── test_ai_inference_pipeline.py
│   └── test_end_to_end.py
└── conftest.py       # Pytest fixtures and configuration
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_drone.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests only
pytest tests/integration/
```

## Test Requirements

- All PR must maintain >80% code coverage
- All tests must pass before merging to development
- Tests must run in <5 minutes

## Continuous Integration

Tests automatically run on every pull request via GitHub Actions.
