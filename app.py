
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Student Information API
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


# Custom API for Additional Task
@app.route("/welcome")
def welcome():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Welcome to the BSIT Student API, {name}!",
        "program": "BSIT",
        "college": "CICI"
    })


if __name__ == "__main__":
    app.run(debug=True)
