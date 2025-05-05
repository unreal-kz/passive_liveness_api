import json
from src.flutter_liveness_verifier.infra.kafka.producer import KafkaLivenessProducer

def test_kafka_serialization():
    payload = {
        "user_id": "testuser",
        "timestamp": "2025-05-05T17:00:00Z",
        "device_id": "device123",
        "liveness_score": 0.99,
        "verdict": "live",
        "session_id": "sess123"
    }
    producer = KafkaLivenessProducer()
    value = json.dumps(payload).encode('utf-8')
    key = payload["user_id"].encode('utf-8')
    assert isinstance(value, bytes)
    assert isinstance(key, bytes)
    assert json.loads(value.decode('utf-8')) == payload
