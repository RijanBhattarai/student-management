"""
================================================================
  Student Management System — Flask Backend
  Author  : Rijan
  Stack   : Python Flask + SQLite
  Features: Full CRUD API for Students, Courses, Enrollments
================================================================
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
import sqlite3
import os
import json
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


# ── Database Setup ────────────────────────────────────────────
def get_db():
    """Return a database connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables and seed sample data if the DB doesn't exist yet."""
    conn = get_db()
    cur  = conn.cursor()

    # Students table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            phone       TEXT,
            dob         TEXT,
            gender      TEXT,
            address     TEXT,
            program     TEXT    NOT NULL,
            year        INTEGER NOT NULL DEFAULT 1,
            gpa         REAL    DEFAULT 0.0,
            status      TEXT    DEFAULT 'Active',
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Courses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            code        TEXT    NOT NULL UNIQUE,
            name        TEXT    NOT NULL,
            credits     INTEGER NOT NULL DEFAULT 3,
            instructor  TEXT,
            semester    TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Enrollments table (junction)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            course_id   INTEGER NOT NULL REFERENCES courses(id)  ON DELETE CASCADE,
            grade       TEXT    DEFAULT 'N/A',
            enrolled_at TEXT    DEFAULT (datetime('now')),
            UNIQUE(student_id, course_id)
        )
    """)

    # Seed data only if tables are empty
    if cur.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        students = [
            ("Aarav Sharma",    "aarav@example.com",   "9801000001", "2002-04-12", "Male",   "Kathmandu",  "BSc Computer Systems Engineering", 3, 3.8, "Active"),
            ("Sita Thapa",      "sita@example.com",    "9802000002", "2003-07-22", "Female", "Pokhara",    "BSc Computer Science",             2, 3.5, "Active"),
            ("Bikram KC",       "bikram@example.com",  "9803000003", "2001-11-05", "Male",   "Biratnagar", "BSc Information Technology",        4, 3.2, "Active"),
            ("Priya Karki",     "priya@example.com",   "9804000004", "2003-02-18", "Female", "Lalitpur",   "BSc Computer Systems Engineering", 2, 3.9, "Active"),
            ("Roshan Shrestha", "roshan@example.com",  "9805000005", "2002-08-30", "Male",   "Chitwan",    "BSc Software Engineering",         3, 3.1, "Active"),
            ("Anita Gurung",    "anita@example.com",   "9806000006", "2004-01-15", "Female", "Kathmandu",  "BSc Computer Science",             1, 3.7, "Active"),
            ("Deepak Rai",      "deepak@example.com",  "9807000007", "2001-06-25", "Male",   "Butwal",     "BSc Information Technology",        4, 2.9, "Inactive"),
            ("Kabita Limbu",    "kabita@example.com",  "9808000008", "2003-09-10", "Female", "Pokhara",    "BSc Software Engineering",         2, 3.6, "Active"),
        ]
        cur.executemany("""
            INSERT INTO students
            (full_name,email,phone,dob,gender,address,program,year,gpa,status)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, students)

    if cur.execute("SELECT COUNT(*) FROM courses").fetchone()[0] == 0:
        courses = [
            ("CET324", "Advanced Cybersecurity",     3, "Dr. Patel",   "Semester 5"),
            ("CET313", "Artificial Intelligence",    3, "Dr. Sharma",  "Semester 5"),
            ("CET341", "Advanced Data Technologies", 3, "Dr. Thapa",   "Semester 6"),
            ("CET201", "Database Systems",           3, "Dr. KC",      "Semester 3"),
            ("CET101", "Programming Fundamentals",   4, "Mr. Gurung",  "Semester 1"),
            ("CET215", "Computer Networks",          3, "Dr. Rai",     "Semester 4"),
            ("CET302", "Web Development",            3, "Mr. Limbu",   "Semester 5"),
            ("CET410", "Software Engineering",       3, "Dr. Karki",   "Semester 7"),
        ]
        cur.executemany("""
            INSERT INTO courses (code,name,credits,instructor,semester)
            VALUES (?,?,?,?,?)
        """, courses)

    if cur.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0] == 0:
        enrollments = [
            (1,1,"A"),(1,2,"B+"),(1,3,"A-"),
            (2,1,"B"),(2,4,"A"),(2,5,"A+"),
            (3,4,"B-"),(3,6,"C+"),(3,7,"B"),
            (4,1,"A+"),(4,2,"A"),(4,3,"A"),
            (5,5,"B+"),(5,6,"B"),(5,7,"C"),
            (6,5,"A"),(6,1,"A-"),
            (7,4,"C"),(7,8,"D"),
            (8,2,"B+"),(8,3,"A-"),(8,7,"B"),
        ]
        cur.executemany("""
            INSERT INTO enrollments (student_id,course_id,grade)
            VALUES (?,?,?)
        """, enrollments)

    conn.commit()
    conn.close()
    print("  Database initialised.")


# ══════════════════════════════════════════════════════════════
# FRONTEND ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


# ══════════════════════════════════════════════════════════════
# STUDENT API ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.route("/api/students", methods=["GET"])
def get_students():
    """Return all students, with optional search by name/program/status."""
    conn    = get_db()
    search  = request.args.get("search", "").strip()
    program = request.args.get("program", "").strip()
    status  = request.args.get("status", "").strip()

    query  = "SELECT * FROM students WHERE 1=1"
    params = []
    if search:
        query  += " AND (full_name LIKE ? OR email LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if program:
        query  += " AND program = ?"
        params.append(program)
    if status:
        query  += " AND status = ?"
        params.append(status)
    query += " ORDER BY full_name"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/students/<int:sid>", methods=["GET"])
def get_student(sid):
    """Return a single student by ID."""
    conn = get_db()
    row  = conn.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(row))


@app.route("/api/students", methods=["POST"])
def add_student():
    """Create a new student record."""
    data = request.get_json()
    required = ["full_name", "email", "program", "year"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    conn = get_db()
    try:
        cur = conn.execute("""
            INSERT INTO students
            (full_name,email,phone,dob,gender,address,program,year,gpa,status)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            data["full_name"], data["email"],
            data.get("phone",""), data.get("dob",""),
            data.get("gender",""), data.get("address",""),
            data["program"], int(data["year"]),
            float(data.get("gpa", 0.0)), data.get("status","Active")
        ))
        conn.commit()
        new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists"}), 409
    conn.close()
    return jsonify({"message": "Student added", "id": new_id}), 201


@app.route("/api/students/<int:sid>", methods=["PUT"])
def update_student(sid):
    """Update an existing student."""
    data = request.get_json()
    conn = get_db()
    row  = conn.execute("SELECT id FROM students WHERE id=?", (sid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute("""
        UPDATE students
        SET full_name=?,email=?,phone=?,dob=?,gender=?,
            address=?,program=?,year=?,gpa=?,status=?
        WHERE id=?
    """, (
        data["full_name"], data["email"],
        data.get("phone",""), data.get("dob",""),
        data.get("gender",""), data.get("address",""),
        data["program"], int(data["year"]),
        float(data.get("gpa",0.0)), data.get("status","Active"),
        sid
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})


@app.route("/api/students/<int:sid>", methods=["DELETE"])
def delete_student(sid):
    """Delete a student and their enrollments."""
    conn = get_db()
    row  = conn.execute("SELECT id FROM students WHERE id=?", (sid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    conn.execute("DELETE FROM enrollments WHERE student_id=?", (sid,))
    conn.execute("DELETE FROM students WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})


# ══════════════════════════════════════════════════════════════
# COURSE API ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.route("/api/courses", methods=["GET"])
def get_courses():
    conn = get_db()
    rows = conn.execute("SELECT * FROM courses ORDER BY code").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/courses", methods=["POST"])
def add_course():
    data = request.get_json()
    conn = get_db()
    try:
        cur = conn.execute("""
            INSERT INTO courses (code,name,credits,instructor,semester)
            VALUES (?,?,?,?,?)
        """, (data["code"], data["name"], int(data.get("credits",3)),
              data.get("instructor",""), data.get("semester","")))
        conn.commit()
        new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Course code already exists"}), 409
    conn.close()
    return jsonify({"message": "Course added", "id": new_id}), 201


@app.route("/api/courses/<int:cid>", methods=["DELETE"])
def delete_course(cid):
    conn = get_db()
    conn.execute("DELETE FROM enrollments WHERE course_id=?", (cid,))
    conn.execute("DELETE FROM courses WHERE id=?", (cid,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Course deleted"})


# ══════════════════════════════════════════════════════════════
# ENROLLMENT API ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.route("/api/students/<int:sid>/enrollments", methods=["GET"])
def get_student_enrollments(sid):
    """Get all courses a student is enrolled in."""
    conn = get_db()
    rows = conn.execute("""
        SELECT e.id, e.grade, e.enrolled_at,
               c.id as course_id, c.code, c.name, c.credits, c.instructor, c.semester
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.student_id = ?
        ORDER BY c.code
    """, (sid,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/enrollments", methods=["POST"])
def enroll_student():
    data = request.get_json()
    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO enrollments (student_id, course_id, grade)
            VALUES (?,?,?)
        """, (data["student_id"], data["course_id"], data.get("grade","N/A")))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Student already enrolled in this course"}), 409
    conn.close()
    return jsonify({"message": "Enrolled successfully"}), 201


@app.route("/api/enrollments/<int:eid>", methods=["DELETE"])
def remove_enrollment(eid):
    conn = get_db()
    conn.execute("DELETE FROM enrollments WHERE id=?", (eid,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Enrollment removed"})


# ══════════════════════════════════════════════════════════════
# DASHBOARD STATS ENDPOINT
# ══════════════════════════════════════════════════════════════

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_db()
    total_students  = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    active_students = conn.execute("SELECT COUNT(*) FROM students WHERE status='Active'").fetchone()[0]
    total_courses   = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    total_enrolled  = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]
    avg_gpa         = conn.execute("SELECT ROUND(AVG(gpa),2) FROM students WHERE status='Active'").fetchone()[0]
    by_program      = conn.execute("""
        SELECT program, COUNT(*) as count FROM students GROUP BY program ORDER BY count DESC
    """).fetchall()
    by_year         = conn.execute("""
        SELECT year, COUNT(*) as count FROM students GROUP BY year ORDER BY year
    """).fetchall()
    conn.close()
    return jsonify({
        "total_students":  total_students,
        "active_students": active_students,
        "total_courses":   total_courses,
        "total_enrolled":  total_enrolled,
        "avg_gpa":         avg_gpa or 0.0,
        "by_program":      [dict(r) for r in by_program],
        "by_year":         [dict(r) for r in by_year],
    })


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    init_db()
    print("  Student Management System running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
