
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my first API!"

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00273",
        "name": "Janeza Ann Arante",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })

@app.route('/course')
def get_course():
    return jsonify({
        "course_name": "Web Development",
        "course_code": "IT101",
        "program": "BSIT"
    })

@app.route('/greeting')
def greeting():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Welcome, {name}!",
        "purpose": "Personalized greeting",
        "status": "Success"
    })

if __name__ == '__main__':
    app.run(debug=True)
