from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Task

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    db = next(get_db())
    tasks = db.query(Task).all()
    return jsonify([{"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "Título y descripción son requeridos"}), 400
    db = next(get_db())
    new_task = Task(title=title, description=description, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return jsonify({"id": new_task.id, "title": new_task.title, "description": new_task.description, "completed": new_task.completed})

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def mark_task_completed(task_id):
    db = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    task.completed = True
    db.commit()
    db.refresh(task)
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "completed": task.completed})

if __name__ == "__main__":
    app.run(debug=True)