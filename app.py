
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# SQLite Database Connection
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Existing Student Information API
@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00273",
        "name": "Janeza Ann Arante",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# Greeting API
@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Custom Welcome API
@app.route("/welcome")
def welcome():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Welcome to the BSIT Student API, {name}!",
        "program": "BSIT",
        "college": "CICI"
    })


# API: Get All Students from SQLite Database
@app.route("/students")
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# API: Get One Student by Database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# Additional Task: Get Students by Program
@app.route("/students/program/<program>")
def get_students_by_program(program):
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students WHERE program = ?",
        (program.upper(),)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == "__main__":
    app.run(debug=True)
