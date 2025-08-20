# Student Management System (Console, Python)

A simple, beginner-friendly console app to manage student records (CRUD).  
Built to practice core Python: functions, lists/dicts, loops, conditionals, and JSON file I/O.

## Run
```bash
python student_mgmt.py
```

## Features
- Add new student
- View all students (pretty table)
- Search student by Roll No
- Update student (press Enter to keep old values)
- Delete student (with confirmation)
- **JSON persistence** via `data.json`

## Data Model
Each student is a dictionary:
```json
{"roll_no": "101", "name": "Alice", "grade": "A", "age": "15"}
```

## Project Structure
```
student-management/
├─ student_mgmt.py
├─ data.json              # created on first save
├─ README.md
└─ tests/
   └─ test_basic.py       
```

## Usage
Follow the on-screen menu:
1) Add Student  
2) View Students  
3) Search Student by Roll No  
4) Update Student  
5) Delete Student  
6) Exit

## Improvements (nice extras)
- Search by name (partial match)
- Sort by roll no or name
- Export to CSV
- Use SQLite for storage
- GUI with Tkinter
- Web app with Flask + Bootstrap
- Unit tests + CI (GitHub Actions)

## What I learned
- Functions & modular design
- Lists/dicts for data modeling
- Input validation and UX
- JSON persistence
