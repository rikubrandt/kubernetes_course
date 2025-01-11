import os
import requests
from flask import Flask, render_template, redirect, url_for, request, send_file
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

TODO_BACKEND_URL = os.getenv("TODO_BACKEND_URL", "http://todo-backend-svc:5000")
IMAGE_URL = "https://picsum.photos/1200"
IMAGE_PATH = "/shared/image.jpg"
CACHE_EXPIRY = timedelta(hours=1)


@app.route("/", methods=["GET"])
def home():
    """Render the todo list and form."""
    todos = fetch_todos()

    if not os.path.exists(IMAGE_PATH) or \
       (datetime.now(timezone.utc) - datetime.fromtimestamp(os.path.getmtime(IMAGE_PATH), timezone.utc) > CACHE_EXPIRY):
        fetch_image()

    return render_template("home.html", todos=todos)


@app.route("/todosent", methods=["POST"])
def add_todo():
    todo_text = request.form.get("todo", "").strip()
    if todo_text and len(todo_text) <= 140:
        try:
            response = requests.post(
                f"{TODO_BACKEND_URL}/todos",
                json={"todo": todo_text},
                timeout=2,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error adding todo: {e}")
    else:
        print("Invalid todo or exceeds 140 characters.")
    return redirect(url_for("home"))


@app.route("/image", methods=["GET"])
def image():
    return send_file(IMAGE_PATH, mimetype="image/jpeg")


def fetch_todos():
    """Fetch the todos from the backend."""
    try:
        response = requests.get(f"{TODO_BACKEND_URL}/todos", timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching todos: {e}")
        return []


def fetch_image():
    try:
        response = requests.get(IMAGE_URL, stream=True)
        response.raise_for_status()
        with open(IMAGE_PATH, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Fetched a new image at {datetime.utcnow().isoformat()}")
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
