from flask import Flask, jsonify
import os

app = Flask(__name__)
counter = 0

@app.route("/pingpong")
def pingpong():
    global counter
    counter += 1
    return f"pong {counter}"

@app.route("/count")
def count():
    return jsonify({"count": counter})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("Ping-Pong Application started")
    app.run(host="0.0.0.0", port=port)
