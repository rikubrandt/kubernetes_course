from flask import Flask
import os

app = Flask(__name__)
counter = 0
OUTPUT_FILE = "/shared/ping_count.txt"

@app.route("/pingpong")
def pingpong():
    global counter
    counter += 1
    with open(OUTPUT_FILE, "w") as file:
        file.write(str(counter))
    return f"pong {counter}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    os.makedirs("/shared", exist_ok=True)
    print("Ping-Pong Application started")
    app.run(host="0.0.0.0", port=port)
