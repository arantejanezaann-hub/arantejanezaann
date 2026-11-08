
import requests 
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row

    # Automatically create students table if it does not exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL
        )
    """)

    conn.commit()

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
    return jsonify({"message": f"Hello, {name}!"})


# Custom Welcome API
@app.route("/welcome")
def welcome():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Welcome to the BSIT Student API, {name}!",
        "program": "BSIT",
        "college": "CICI"
    })


# READ: Get All Students
@app.route("/students")
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# READ: Get One Student by Database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# READ: Get Students by Program
@app.route("/students/program/<program>")
def get_students_by_program(program):
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students WHERE UPPER(program) = ?",
        (program.upper(),)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# STEP 2: CREATE - Add Student
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    required = ["student_id", "name", "program", "year", "section"]

    if any(data.get(field) in (None, "") for field in required):
        return jsonify({"error": "Please complete all fields"}), 400

    try:
        conn = get_db_connection()

        cursor = conn.execute(
            """INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)""",
            (
                data["student_id"],
                data["name"],
                data["program"],
                int(data["year"]),
                data["section"]
            )
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Student added successfully!",
            "id": new_id
        }), 201

    except (ValueError, sqlite3.Error) as e:
        return jsonify({"error": str(e)}), 400


# STEP 3: READ - Get One Student through CRUD API
@app.route("/api/students/<int:id>", methods=["GET"])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# READ: Get All Students for Classmate's API
@app.route("/api/students", methods=["GET"])
def api_students():
    conn = get_db_connection()

    rows = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# STEP 3: UPDATE - Edit Student
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    required = ["student_id", "name", "program", "year", "section"]

    if any(data.get(field) in (None, "") for field in required):
        return jsonify({"error": "Please complete all fields"}), 400

    try:
        conn = get_db_connection()

        cursor = conn.execute(
            """UPDATE students
            SET student_id=?, name=?, program=?,
            year=?, section=?
            WHERE id=?""",
            (
                data["student_id"],
                data["name"],
                data["program"],
                int(data["year"]),
                data["section"],
                id
            )
        )

        conn.commit()
        updated = cursor.rowcount
        conn.close()

        if updated == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student updated successfully!"})

    except (ValueError, sqlite3.Error) as e:
        return jsonify({"error": str(e)}), 400


# STEP 3: DELETE - Remove Student
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?", (id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully!"})

# RETRIEVE CLASSMATE'S RECORDS THROUGH YOUR FLASK SERVER
@app.route("/api/classmate-students")
def get_classmate_students():

    classmate_api = "https://agagdangerich-1.onrender.com/api/students"

    try:
        response = requests.get(classmate_api, timeout=30)
        response.raise_for_status()

        students = response.json()

        if not isinstance(students, list):
            return jsonify({
                "error": "Classmate API did not return a list of students"
            }), 502

        return jsonify(students)

    except requests.RequestException as e:
        return jsonify({
            "error": "Unable to connect to classmate API",
            "details": str(e)
        }), 502

    except ValueError:
        return jsonify({
            "error": "Classmate API returned invalid JSON"
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
