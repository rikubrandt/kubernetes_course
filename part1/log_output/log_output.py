import time
import random
from datetime import datetime
import string
from flask import Flask, jsonify

app = Flask(__name__)

random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
current_timestamp = datetime.now()

@app.route("/")
def home():
    return "Log Output APP."

@app.route("/status")
def status():
    return jsonify({
        "timestamp": current_timestamp,
        "random_string": random_string
    })

if __name__ == "__main__":
    print(f"Server started with random string: {random_string}")
    app.run(host="0.0.0.0", port=5000)

