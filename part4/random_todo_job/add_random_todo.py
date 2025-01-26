import os
import requests

TODO_BACKEND_URL = os.getenv("TODO_BACKEND_URL", "http://todo-backend-svc:5000")
WIKIPEDIA_RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"

def fetch_random_wikipedia_url():
    """Fetch a random Wikipedia URL."""
    try:
        response = requests.head(WIKIPEDIA_RANDOM_URL, allow_redirects=True, timeout=5)
        response.raise_for_status()
        return response.url
    except requests.RequestException as e:
        print(f"Error fetching Wikipedia article: {e}")
        return None

def add_todo(todo_text):
    """Add a new todo via the backend."""
    try:
        response = requests.post(
            f"{TODO_BACKEND_URL}/todos",
            json={"todo": todo_text},
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print(f"Added todo: {todo_text}")
    except requests.RequestException as e:
        print(f"Error adding todo: {e}")

if __name__ == "__main__":
    wikipedia_url = fetch_random_wikipedia_url()
    if wikipedia_url:
        todo_text = f"Read {wikipedia_url}"
        add_todo(todo_text)
