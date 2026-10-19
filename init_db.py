
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

# Reset the sample records each time this file runs
cursor.execute("DELETE FROM students")

students = [
    ("24-00316", "Erich Agagadang", "BSIT", 3, "A"),
    ("24-00453", "Jessica Ann Balcena", "BSIT", 3, "B"),
    ("24-00111", "Jm Abordaje", "BSIT", 3, "A"),
    ("24-00145", "Mariel Alda", "BSIT", 3, "A"),
    ("24-00678", "Necole Aloro", "BSIT", 3, "A")
]

cursor.executemany("""
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database created successfully.")
