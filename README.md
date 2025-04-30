# Passive Liveness API

A modular, production-ready Python backend for passive liveness detection in mobile onboarding.

## Purpose
Receives a base64-encoded RGB face image and determines if the face is real or spoofed using a pretrained SilentFaceLiveness model. Supports fallback to active liveness detection if the passive check is inconclusive.

## Architecture Overview
- **API Layer (`api/`)**: FastAPI endpoints and request/response schemas.
- **Model Loader (`models/`)**: Factory pattern for loading ONNX or PyTorch models. Model interface and adapters for extensibility.
- **Evaluation (`evaluation/`)**: Strategy pattern for threshold-based liveness decision logic.
- **Fallback (`fallback/`)**: Interface/Adapter for triggering active liveness checks (e.g., blink, head-turn).
- **Configuration (`config.py`)**: Centralized, adjustable parameters (e.g., threshold).
- **Bootstrap (`main.py`)**: Application entrypoint.
- **Tests (`tests/`)**: Placeholder for test utilities and future coverage.

## SOLID & Design Patterns
- **Factory**: Model loader for ONNX/PyTorch.
- **Strategy**: Threshold-based evaluation logic.
- **Adapter/Interface**: Fallback mechanism for active checks.

## Inputs
- `image_base64`: str (base64-encoded RGB face image)
- `model_type`: Optional[str] = "onnx" or "pytorch"

## Outputs
- JSON response:
  - `liveness_label`: "real" or "fake"
  - `confidence_score`: float (0.0–1.0)
  - `requires_active_check`: bool (True if confidence < threshold)

## Extensibility
- Add new models, evaluation strategies, or fallback mechanisms by extending respective modules.

---

This project is a scalable foundation for production-grade liveness detection APIs. See module docstrings for further details.
