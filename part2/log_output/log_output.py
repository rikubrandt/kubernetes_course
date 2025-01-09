import os
import hashlib
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

PINGPONG_URL = os.getenv("PINGPONG_URL", "http://ping-pong-svc:5000/count")

@app.route("/")
def home():
    """Fetch the pong count from Ping-Pong Application and display the log output."""
    try:
        response = requests.get(PINGPONG_URL, timeout=2)
        response.raise_for_status()
        count = response.json().get("count", 0)
    except requests.RequestException as e:
        count = "Error fetching pong count"
        print(f"Error: {e}")

    timestamp = datetime.utcnow().isoformat()
    hashed_timestamp = hashlib.sha256(timestamp.encode()).hexdigest()

    return f"{timestamp}: {hashed_timestamp}. Ping / Pongs: {count}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("Log Output Application started")
    app.run(host="0.0.0.0", port=port)
