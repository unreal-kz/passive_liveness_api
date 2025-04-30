# Passive Liveness API

## Project Overview
- Python FastAPI service for passive liveness detection in onboarding workflows.
- Modular, extensible design: model loading, inference, fallback, and HTTP layers.
- [Architecture diagram](link-to-diagram-or-placeholder)

## Quick-start
- Clone the repo
- Create and activate a virtualenv (Python 3.10+)
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Start the API server:
  ```sh
  uvicorn passive_liveness_api.main:app --reload
  ```

## Local Smoke Test
- Confirm the scaffold works end-to-end:
  ```sh
  python test_script.py --image samples/sample1.jpg --model-type onnx
  ```
- Output is a placeholder until real ML logic is added.

## API Reference
### POST /liveness
- Accepts: JSON with base64-encoded face image
- Returns: JSON with liveness label, confidence, and fallback if needed

#### Example request
```json
{
  "image": "<base64-string>"
}
```

#### Example response
```json
{
  "liveness_label": "real",
  "confidence_score": 0.99,
  "requires_active_check": false
}
```

## Roadmap / TODO
- Implement real model loading and inference logic
- Add image preprocessing utilities
- Integrate active fallback checks
- Expand unit/integration test coverage
- Add CI/CD and deployment scripts
