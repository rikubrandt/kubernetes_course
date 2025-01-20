import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Retrieve credentials from environment variables
DATABASE_USER = os.getenv("DATABASE_USER", "defaultuser")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "defaultpassword")
DATABASE_NAME = os.getenv("DATABASE_NAME", "defaultdb")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")

# Construct the database URL
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}"

def get_connection():
    """Establish and return a connection to the database."""
    return psycopg2.connect(DATABASE_URL)

def initialize_db():
    """Create the counaer table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS counter (id SERIAL PRIMARY KEY, value INT DEFAULT 0);")
    cursor.execute("INSERT INTO counter (value) SELECT 0 WHERE NOT EXISTS (SELECT * FROM counter);")
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Ping-Pong application is running. Use /pingpong or /count."})

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for GCP Ingress."""
    return jsonify({"status": "healthy"}), 200

@app.route("/pingpong", methods=["GET"])
def handle_pingpong():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE counter SET value = value + 1;")
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Ping / Pong counter incremented!"})
    except Exception as e:
        print(f"Error handling /pingpong: {e}")
        return jsonify({"message": "Error incrementing ping/pong counter."})
    
@app.route("/count", methods=["GET"])
def get_count():
    """Retrieve the counter value from the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM counter LIMIT 1;")
        value = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"count": value})
    except Exception as e:
        print(f"Error retrieving counter: {e}")
        return jsonify({"count": "Error"})

if __name__ == "__main__":
    initialize_db()
    port = int(os.getenv("PORT", 5000))
    print("Log Output Application started")
    app.run(host="0.0.0.0", port=port)
