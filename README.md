# 🎓 Student Management System — Full Stack

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![HTML](https://img.shields.io/badge/HTML5-CSS3-orange?logo=html5)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

A full-stack **Student Management System** built with Python Flask (REST API backend), SQLite (database), and vanilla HTML/CSS/JavaScript (frontend). Features a live dashboard, full CRUD operations, search & filter, and student enrollment management.

---

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Screenshots](#screenshots)
- [Skills Demonstrated](#skills-demonstrated)

---

## Features

### Dashboard
- KPI cards: Total Students, Active Students, Total Courses, Average GPA
- Students by Program — CSS bar chart
- Students by Year — CSS bar chart

### Student Management
- Add, Edit, Delete students
- Live search by name or email
- Filter by program and status
- GPA colour coding (green/amber/red)
- Active/Inactive status badges

### Course Management
- Add and Delete courses
- View code, name, credits, instructor, semester

### Enrollment Management
- Enroll students in courses
- View all courses a student is enrolled in
- Record and display grades
- Remove enrollments

### General
- Toast notifications for all actions
- Confirm dialog before delete
- Responsive sidebar navigation
- Clean modal forms with validation

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python Flask — REST API with JSON responses |
| **Database** | SQLite — 3 tables (students, courses, enrollments) |
| **Frontend** | HTML5, CSS3 (CSS variables, grid, flexbox) |
| **JavaScript** | Vanilla ES6 (fetch API, async/await, DOM manipulation) |
| **Icons** | Font Awesome 6 (CDN) |

---

## Project Structure

```
student-management/
│
├── backend/
│   ├── app.py              Flask REST API + DB init + all routes
│   └── database.db         SQLite database (auto-created on first run)
│
├── frontend/
│   ├── templates/
│   │   └── index.html      Main SPA template served by Flask
│   └── static/
│       ├── css/
│       │   └── style.css   Full custom stylesheet
│       └── js/
│           └── app.js      Frontend logic (fetch, DOM, events)
│
├── requirements.txt        Python dependencies
└── README.md               This file
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/RijanBhattarai/student-management.git
cd student-management

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the Flask server
python backend/app.py

# 4. Open in browser
# http://127.0.0.1:5000
```

The database is created automatically with sample data on first run.

---

## API Reference

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students` | List all students (supports `?search=`, `?program=`, `?status=`) |
| GET | `/api/students/:id` | Get single student |
| POST | `/api/students` | Add new student |
| PUT | `/api/students/:id` | Update student |
| DELETE | `/api/students/:id` | Delete student |

### Courses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses` | List all courses |
| POST | `/api/courses` | Add new course |
| DELETE | `/api/courses/:id` | Delete course |

### Enrollments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/:id/enrollments` | Get student enrollments |
| POST | `/api/enrollments` | Enroll student in course |
| DELETE | `/api/enrollments/:id` | Remove enrollment |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Summary stats for dashboard |

---

## Skills Demonstrated

- **REST API Design** — Clean endpoint structure with proper HTTP methods and status codes
- **Flask** — Routing, JSON responses, static file serving, template rendering
- **SQLite** — Schema design (3NF), foreign keys, CASCADE delete, parameterised queries
- **JavaScript (ES6)** — fetch API, async/await, DOM manipulation, event listeners
- **Single Page Application** — Client-side routing without page reloads
- **CRUD Operations** — Full Create, Read, Update, Delete for students and courses
- **Form Validation** — Client-side and server-side validation with error messages
- **CSS Architecture** — CSS variables, grid, flexbox, responsive layout, modal system

---

