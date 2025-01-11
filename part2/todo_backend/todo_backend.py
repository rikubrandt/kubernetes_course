from flask import Flask, jsonify, request

app = Flask(__name__)
todos = []  

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "todo" not in data:
        return jsonify({"error": "Invalid request"}), 400
    todo = data["todo"]
    todos.append(todo)
    return jsonify({"message": "Todo added", "todo": todo}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
