# Passive Liveness API

## Project Overview
- Python FastAPI service for passive liveness detection in onboarding workflows.
- Modular, extensible design: model loading, inference, fallback, and HTTP layers.
- [Architecture diagram](link-to-diagram-or-placeholder)

## Prerequisites
- Python 3.10+
- For best face detection, install MediaPipe (CPU-only):
  ```sh
  pip install mediapipe
  ```
  - MediaPipe may require extra system wheels on some platforms; see [MediaPipe install docs](https://google.github.io/mediapipe/getting_started/install.html).
  - If MediaPipe is not available, OpenCV Haarcascade will be used as a fallback.

## Quick-start
- Clone the repo
- Create and activate a virtualenv (Python 3.10+)
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- **Download the SilentFaceLiveness ONNX model weights**:
  - Get the official ONNX file from the [SilentFaceLiveness repository](https://github.com/zhangchuheng123/Silent-Face-Anti-Spoofing).
  - Place the model at `models/silentface.onnx` **or** set the `MODEL_PATH` environment variable to the ONNX file location.
- Start the API server:
  ```sh
  uvicorn passive_liveness_api.main:app --reload
  ```
- Now, POSTing a real face image to `/liveness` will return a true confidence score.

## Active Blink Challenge Flow
1. **Step 1:** Client POSTs a face image to `/liveness`.
    - If passive liveness is inconclusive, the response includes a `fallback` with `challenge_type: "blink"` and an `upload_url`.
2. **Step 2:** Client POSTs a short video (3-5s, showing a blink) to `/active/blink` (as `multipart/form-data` with `video` field).
3. **Step 3:** Server analyzes the video and responds with `{ "active_passed": true/false }`.

This two-step flow ensures robust liveness detection by combining passive and active (blink) checks.

## Run with Docker
- Build the image:
  ```sh
  docker build -t passive_liveness_api .
  ```
- Run the container:
  ```sh
  docker run -p 8000:8000 passive_liveness_api
  ```
- Or use docker-compose:
  ```sh
  docker-compose up --build
  ```
- Test the API:
  ```sh
  curl -X POST "http://localhost:8000/liveness" -H "Content-Type: application/json" -d '{"image":"<base64-string>"}'
  ```

## Authentication
- If `API_KEY` is set, every request must include either:
  - `X-API-KEY` header: `-H "X-API-KEY: my-secret"`
  - or Bearer token: `-H "Authorization: Bearer my-secret"`
- Example:
  ```sh
  curl -X POST "http://localhost:8000/liveness" \
    -H "Content-Type: application/json" \
    -H "X-API-KEY: my-secret" \
    -d '{"image":"<base64-string>"}'
  ```
- Or with bearer:
  ```sh
  curl -X POST "http://localhost:8000/liveness" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer my-secret" \
    -d '{"image":"<base64-string>"}'
  ```
- If the header or token is missing/invalid, the API returns 401 Unauthorized.

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
