import os
import psycopg2
from flask import Flask, jsonify, request
import logging
import time

app = Flask(__name__)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
HOST = "postgres-svc"
PORT = 5432

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}"
logging.basicConfig(
    level=logging.INFO,  # Adjust log level as needed
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Send logs to stdout for Loki/Promtail
)
logger = logging.getLogger(__name__)


def get_connection_with_retry(max_retries=10, delay=5):
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            return conn
        except psycopg2.OperationalError as e:
            print(f"DB not ready (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise
            time.sleep(delay)
            
def get_connection():
    """Establish a connection to the database."""
    return psycopg2.connect(DATABASE_URL)

def initialize_db():
    """Initialize the database with a todos table."""
    conn = get_connection_with_retry()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            todo TEXT NOT NULL,
            done BOOLEAN DEFAULT false
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for readiness probes."""
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy"}), 500

@app.route("/todos", methods=["GET"])
def get_todos():
    """Fetch all todos from the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, todo, done FROM todos;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        todos = [
            {"id": row[0], "todo": row[1], "done": row[2]} 
            for row in rows
        ]
        return jsonify(todos)
    except Exception as e:
        print(f"Error fetching todos: {e}")
        return jsonify([]), 500

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update the 'done' status (and possibly other fields) of a todo."""
    data = request.get_json()
    if not data or "done" not in data:
        return jsonify({"error": "Invalid request"}), 400

    done_value = bool(data["done"])

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET done = %s WHERE id = %s;", (done_value, todo_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Todo updated", "id": todo_id, "done": done_value}), 200
    except Exception as e:
        print(f"Error updating todo: {e}")
        return jsonify({"error": "Failed to update todo"}), 500


@app.route("/todos", methods=["POST"])
def add_todo():
    """Add a new todo to the database."""
    data = request.get_json()
    if not data or "todo" not in data:
        return jsonify({"error": "Invalid request"}), 400

    todo = data["todo"]

    if len(todo) > 140:
        logger.warning(f"Todo rejected: {todo[:50]}... (exceeds 140 characters)")
        return jsonify({"error": "Todo exceeds 140 characters"}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (todo) VALUES (%s);", (todo,))
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"New todo added: {todo}")
        return jsonify({"message": "Todo added", "todo": todo}), 201
    except Exception as e:
        print(f"Error adding todo: {e}")
        logger.warning(f"Error adding todo: {e}")

        return jsonify({"error": "Failed to add todo"}), 500

if __name__ == "__main__":
    print(DATABASE_URL)
    initialize_db()
    app.run(host="0.0.0.0", port=5000)
