import os
import requests
from flask import Flask, send_file, render_template_string
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

IMAGE_URL = "https://picsum.photos/1200"
IMAGE_PATH = "/shared/image.jpg"
CACHE_EXPIRY = timedelta(hours=1)

todos = ["Todo 1", "TODO 2", "TODO 3"]

def fetch_image():
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
    if not os.path.exists(IMAGE_PATH) or \
       (datetime.now(timezone.utc) - datetime.fromtimestamp(os.path.getmtime(IMAGE_PATH), timezone.utc) > CACHE_EXPIRY):
        fetch_image()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            input { width: 300px; padding: 5px; margin: 5px 0; }
            button { padding: 5px 10px; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 5px 0; }
            img { max-width: 100%; height: auto; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Create Todos</h1>
        <form id="todoForm" onsubmit="return false;">
            <input type="text" id="todoInput" maxlength="140" placeholder="Enter a todo (max 140 chars)">
            <button type="button" onclick="addTodo()">Send</button>
        </form>
        <h2>List:</h2>
        <ul id="todoList">
            {% for todo in todos %}
                <li>{{ todo }}</li>
            {% endfor %}
        </ul>
        <h2>Random Hourly Image:</h2>
        <img src="/image" alt="Random Image">

        <script>
            function addTodo() {
                const todoInput = document.getElementById("todoInput");
                const todoText = todoInput.value.trim();
                if (todoText) {
                    const todoList = document.getElementById("todoList");
                    const newTodo = document.createElement("li");
                    newTodo.textContent = todoText;
                    todoList.appendChild(newTodo);
                    todoInput.value = "";
                } else {
                    alert("Please enter a valid todo.");
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, todos=todos)

@app.route("/image")
def image():
    """Serve the cached image."""
    return send_file(IMAGE_PATH, mimetype="image/jpeg")

if __name__ == "__main__":
    os.makedirs("/shared", exist_ok=True)
    print("Todo App started")
    app.run(host="0.0.0.0", port=5000)
