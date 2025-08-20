#!/usr/bin/env python3
"""
Student Management System (Console)
-----------------------------------
Features:
- Add student
- View all students (pretty table)
- Search by Roll No
- Update student (press Enter to keep current value)
- Delete student (with confirmation)
- JSON persistence (data.json)

Data model (each student):
{
  "roll_no": "101",
  "name": "Alice",
  "grade": "A",
  "age": "15"
}
"""

import json
import os
from json import JSONDecodeError

# ---- Persistence config ------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# ---- In-memory store ---------------------------------------------------------
students = []  # list[dict] of students


# ---- Utilities ---------------------------------------------------------------
def load_data():
    """Load students from data.json (if it exists)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            print("⚠️  data.json had unexpected content. Starting with an empty list.")
            return []
    except (JSONDecodeError, OSError):
        print("⚠️  Could not read data.json (maybe it's empty or corrupted). Starting fresh.")
        return []


def save_data():
    """Save students to data.json."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2, ensure_ascii=False)
    except OSError:
        print("❌ Could not save to data.json. Changes only in memory this time.")


def pause():
    input("\nPress Enter to continue...")


def prompt_nonempty(label):
    """Ask until user provides a non-empty value."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def prompt_optional(label):
    """Optional input (can be empty). Returns str (possibly '')."""
    return input(f"{label}: ").strip()


def validate_grade(g):
    """Very light validation for grade; accept anything non-empty but suggest A–F."""
    if not g:
        return False
    # You can make this stricter if you want:
    # return g.upper() in {"A", "B", "C", "D", "E", "F"}
    return True


def search_by_roll(roll_no):
    """Return the first student dict with given roll_no, or None."""
    for s in students:
        if s["roll_no"] == roll_no:
            return s
    return None


def print_table(records):
    """Pretty-print a list of student dicts."""
    if not records:
        print("No records found.")
        return

    # Column headers
    print("")
    print(f"{'Roll No':<10} {'Name':<20} {'Grade':<8} {'Age':<5}")
    print("-" * 47)

    # Rows
    for s in records:
        print(f"{s.get('roll_no',''):<10} {s.get('name',''):<20} {s.get('grade',''):<8} {s.get('age',''):<5}")

    print(f"\nTotal: {len(records)} record(s).")


# ---- CRUD Operations ---------------------------------------------------------
def add_student():
    print("\n➕ Add Student")
    roll = prompt_nonempty("Enter Roll No")
    # Check duplicate
    if search_by_roll(roll):
        print("❌ A student with that roll number already exists.")
        return

    name = prompt_nonempty("Enter Name")
    grade = prompt_nonempty("Enter Grade (e.g., A/B/C...)")
    if not validate_grade(grade):
        print("❌ Invalid grade. Try again (e.g., A/B/C...).")
        return
    age = prompt_optional("Enter Age")

    students.append({
        "roll_no": roll,
        "name": name,
        "grade": grade.upper(),
        "age": age,
    })
    save_data()
    print("✅ Student added successfully!")


def view_students():
    print("\n📋 All Students")
    print_table(students)


def search_student():
    print("\n🔎 Search Student by Roll No")
    roll = prompt_nonempty("Enter Roll No to search")
    s = search_by_roll(roll)
    if s:
        print("\nFound:")
        print_table([s])
    else:
        print("❌ No student found with that roll number.")


def update_student():
    print("\n✏️  Update Student")
    roll = prompt_nonempty("Enter Roll No to update")
    s = search_by_roll(roll)
    if not s:
        print("❌ No student found with that roll number.")
        return

    print("\nCurrent values (press Enter to keep the same):")
    new_name = input(f"Name [{s['name']}]: ").strip()
    new_grade = input(f"Grade [{s['grade']}]: ").strip()
    new_age = input(f"Age [{s.get('age','')}]: ").strip()

    if new_name:
        s["name"] = new_name
    if new_grade:
        if not validate_grade(new_grade):
            print("❌ Invalid grade. Update canceled.")
            return
        s["grade"] = new_grade.upper()
    if new_age or new_age == "":  # allow clearing
        s["age"] = new_age

    save_data()
    print("✅ Student updated successfully!")


def delete_student():
    print("\n🗑️  Delete Student")
    roll = prompt_nonempty("Enter Roll No to delete")
    s = search_by_roll(roll)
    if not s:
        print("❌ No student found with that roll number.")
        return

    confirm = input(f"Are you sure you want to delete {s['name']} (Roll {s['roll_no']})? (y/N): ").strip().lower()
    if confirm == "y":
        students.remove(s)
        save_data()
        print("✅ Student deleted.")
    else:
        print("Deletion canceled.")


# ---- Menu Loop ---------------------------------------------------------------
def print_menu():
    print("""
===============================
🎓 Student Management System
===============================
1) Add Student
2) View Students
3) Search Student by Roll No
4) Update Student
5) Delete Student
6) Exit
""")


def main():
    # Load persisted data at start
    global students
    students = load_data()

    while True:
        try:
            print_menu()
            choice = input("Choose an option (1-6): ").strip()
            if choice == "1":
                add_student()
                pause()
            elif choice == "2":
                view_students()
                pause()
            elif choice == "3":
                search_student()
                pause()
            elif choice == "4":
                update_student()
                pause()
            elif choice == "5":
                delete_student()
                pause()
            elif choice == "6":
                print("👋 Goodbye!! Your data has been saved to data.json.")
                save_data()
                break
            else:
                print("Please choose a valid option (1-6).")
        except KeyboardInterrupt:
            print("\n\n⛔ Interrupted. Saving and exiting...")
            save_data()
            break
        except EOFError:
            print("\n\n⛔ Input ended. Saving and exiting...")
            save_data()
            break


if __name__ == "__main__":
    main()
