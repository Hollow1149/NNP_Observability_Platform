import requests
import time
import random

API_URL = "http://localhost:8000"


def send_dummy_data():
    while True:
        try:
            # 1. Send a synthetic log
            log_payload = {
                "level": random.choice(["info", "debug", "warning"]),
                "source": "synthetic_generator",
                "message": f"Simulated event pulse {random.randint(1000, 9999)}",
                "data": {"internal_id": random.random()},
            }
            requests.post(f"{API_URL}/logs", json=log_payload)

            # 2. Send a synthetic metric
            metric_payload = {
                "name": "synthetic_heartbeat",
                "value": random.uniform(0, 100),
                "tags": {"version": "1.0.0", "region": "mock-zone"},
            }
            requests.post(f"{API_URL}/metrics", json=metric_payload)

            print(f"Sent synthetic pulse at {time.strftime('%H:%M:%S')}")
            time.sleep(5)  # Send every 5 seconds
        except Exception as e:
            print(f"Waiting for pipeline: {e}")
            time.sleep(2)


if __name__ == "__main__":
    send_dummy_data()
