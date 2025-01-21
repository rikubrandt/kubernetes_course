import os
import psycopg2
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

logging.basicConfig(
    level=logging.INFO,  # Adjust log level as needed
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Send logs to stdout for Loki/Promtail
)
logger = logging.getLogger(__name__)


def get_connection():
    """Establish a connection to the database."""
    return psycopg2.connect(DATABASE_URL)

def initialize_db():
    """Initialize the database with a todos table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            todo TEXT NOT NULL
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
        cursor.execute("SELECT todo FROM todos;")
        todos = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(todos)
    except Exception as e:
        print(f"Error fetching todos: {e}")
        return jsonify([]), 500

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
    initialize_db()
    app.run(host="0.0.0.0", port=5000)
