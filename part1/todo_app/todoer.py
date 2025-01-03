from flask import Flask
import os


app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TODO</title>
    </head>
    <body>
        <h1>Welcome to the TODOTODO todo App!</h1>
        <p>Kubernetes is fun!</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Server started in port {port}")
    app.run(host="0.0.0.0", port=port)