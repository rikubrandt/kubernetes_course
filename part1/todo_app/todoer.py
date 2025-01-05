import os
import requests
from flask import Flask, send_file, render_template_string
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
IMAGE_URL = "https://picsum.photos/1200"
IMAGE_PATH = "/shared/image.jpg"
CACHE_EXPIRY = timedelta(hours=1)

def fetch_image():
    """Fetch a new random image from Lorem Picsum and save it to the shared volume."""
    response = requests.get(IMAGE_URL, stream=True)
    if response.status_code == 200:
        with open(IMAGE_PATH, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Fetched a new image at {datetime.utcnow().isoformat()}")
    else:
        print(f"Failed to fetch image: {response.status_code}")

@app.route("/")
def home():
    """Display the cached image in a simple HTML page."""
    # Check if the image needs to be updated
    if not os.path.exists(IMAGE_PATH) or \
       (datetime.now(timezone.utc) - datetime.fromtimestamp(os.path.getmtime(IMAGE_PATH), timezone.utc) > CACHE_EXPIRY):
        fetch_image()

    # Render the image in an HTML page
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo App</title>
    </head>
    <body>
        <h1>Welcome to the Todo App!</h1>
        <p>Here's your hourly random image:</p>
        <img src="/image" alt="Random Image" style="max-width:100%; height:auto;">
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/image")
def image():
    """Serve the cached image."""
    return send_file(IMAGE_PATH, mimetype="image/jpeg")

if __name__ == "__main__":
    os.makedirs("/shared", exist_ok=True)  # Ensure the shared directory exists
    print("Todo App started")
    app.run(host="0.0.0.0", port=5000)
