import os
import json
import time
from confluent_kafka import Producer, KafkaError
from threading import Lock

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092")
KAFKA_TOPIC = "liveness-verified"

class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=30):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure = 0
        self.lock = Lock()
        self.open = False

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.open and (time.time() - self.last_failure < self.reset_timeout):
                raise Exception("Kafka circuit breaker is open")
            try:
                result = func(*args, **kwargs)
                self.failure_count = 0
                self.open = False
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure = time.time()
                if self.failure_count >= self.max_failures:
                    self.open = True
                raise e

circuit_breaker = CircuitBreaker()

class KafkaLivenessProducer:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': KAFKA_BROKERS})

    def publish(self, user_id: str, payload: dict, max_retries=3, backoff_base=0.5):
        value = json.dumps(payload).encode('utf-8')
        key = user_id.encode('utf-8')
        attempt = 0
        while attempt < max_retries:
            try:
                def delivery_report(err, msg):
                    if err is not None:
                        raise KafkaError(err)
                circuit_breaker.call(self.producer.produce, KAFKA_TOPIC, value=value, key=key, callback=delivery_report)
                self.producer.flush()
                return True
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Kafka publish failed after {max_retries} attempts: {e}")
                    return False
                time.sleep(backoff_base * (2 ** attempt))
                attempt += 1
        return False

def publish_liveness_verified(payload: dict):
    producer = KafkaLivenessProducer()
    user_id = payload.get("user_id", "unknown")
    return producer.publish(user_id, payload)
