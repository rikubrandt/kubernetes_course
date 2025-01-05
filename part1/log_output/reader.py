import hashlib
from flask import Flask, jsonify
import os

app = Flask(__name__)
INPUT_FILE = "/shared/timestamp.txt"

@app.route("/")
def home():
    try:
        with open(INPUT_FILE, "r") as file:
            timestamp = file.read().strip()
        hashed_timestamp = hashlib.sha256(timestamp.encode()).hexdigest()
        return jsonify({
            "timestamp": timestamp,
            "hash": hashed_timestamp
        })
    except FileNotFoundError:
        return jsonify({"error": "Timestamp file not found"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("Reader: Started")
    app.run(host="0.0.0.0", port=port)
