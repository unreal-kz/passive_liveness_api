FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "src.flutter_liveness_verifier.main:app", "--host", "0.0.0.0", "--port", "8000"]
