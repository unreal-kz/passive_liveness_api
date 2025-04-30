FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=path/to/model.onnx \
    CONFIDENCE_THRESHOLD=0.85 \
    ENABLE_FALLBACK=true
WORKDIR /app
RUN adduser --disabled-password --gecos '' appuser && chown appuser /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "passive_liveness_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
