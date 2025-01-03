from flask import Flask
import os


app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return "Server is running!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Server started in port {port}")
    app.run(host="0.0.0.0", port=port)