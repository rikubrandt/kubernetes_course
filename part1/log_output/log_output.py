import os
import hashlib
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
INPUT_FILE = "/shared/ping_count.txt"

@app.route("/")
def home():
    try:
        with open(INPUT_FILE, "r") as file:
            ping_count = file.read().strip()
    except FileNotFoundError:
        ping_count = "0"

    timestamp = datetime.utcnow().isoformat()
    hashed_timestamp = hashlib.sha256(timestamp.encode()).hexdigest()
    return f"{timestamp}: {hashed_timestamp}. Ping / Pongs: {ping_count}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    os.makedirs("/shared", exist_ok=True)
    print("Log Output Application started")
    app.run(host="0.0.0.0", port=port)
