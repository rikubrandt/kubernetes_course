from flask import Flask
import os

app = Flask(__name__)
counter = 0

@app.route("/pingpong")
def pingpong():
    global counter
    counter += 1
    return f"pong {counter}"

if __name__ == "__main__":
    print("Ping-Pong Application started")
    app.run(host="0.0.0.0", port=5000)
