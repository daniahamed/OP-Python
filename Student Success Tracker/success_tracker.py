import sqlite3
import rich
from rich.console import Console
from rich.table import Table
import argparse
import datetime
import re

def init_db():
    with sqlite3.connect("success_tracker.db") as conn:
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    major TEXT NOT NULL,
                    gpa REAL CHECK (gpa BETWEEN 0 AND 4),
                    status TEXT CHECK (status IN ('active','probation','graduated')) DEFAULT 'active',
                    last_updated TEXT)
        """)
        print("---Students Table Created---")

def add_student(name: str, email:str, major:str, gpa:float, status:str = "active"):
    valid_status = ['active','probation','graduated']
    if not ( 0<= gpa <=4 ):
        raise ValueError("GPA is out of range")
    
    if status not in valid_status:
        raise ValueError("Invalid status")
    
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.com"
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")

    
    last_updated = datetime.datetime.now().isoformat("T", "seconds")

    with sqlite3.connect("success_tracker.db") as conn:
        cursor = conn.execute(
            """INSERT INTO students(name, email, major, gpa, status, last_updated)
            VALUES(?, ?, ?, ?, ?, ?)""", (name, email, major, gpa, status, last_updated)
        )
        return cursor.lastrowid

def list_students(status:str = None):
    valid_status = ['active','probation','graduated']
    
    
    with sqlite3.connect("success_tracker.db") as conn:
        conn.row_factory = sqlite3.Row
        if status:
            if status not in valid_status:
                raise ValueError("Invalid status")
            
            cursor = conn.execute(
                "SELECT * FROM students WHERE status = ? ORDER BY gpa DESC", (status,)
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM students ORDER BY gpa DESC"
            )
        return cursor.fetchall()
    
def find_students_in_major(major:str):
    with sqlite3.connect("success_tracker.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM students WHERE major = ?",(major,)
        )
        return cursor.fetchall()
        
def update_student_gpa(id: int, gpa:float):
    if not ( 0<= gpa <=4 ):
        raise ValueError("GPA is out of range")
    
    last_updated = datetime.datetime.now().isoformat("T", "seconds")
    
    with sqlite3.connect("success_tracker.db") as conn:
        cursor = conn.execute(
            "UPDATE students SET gpa = ?, last_updated = ? WHERE id = ?", (gpa, last_updated, id)
        )
        return cursor.rowcount
    
def delete_student(id:int):
    with sqlite3.connect("success_tracker.db") as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?", (id,)
        )
        return cursor.rowcount
    
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")

start_db = subparser.add_parser("init_db")

add = subparser.add_parser("add")
add.add_argument("--name", required=True, type=str)
add.add_argument("--email", required=True, type=str)
add.add_argument("--major", required=True, type=str)
add.add_argument("--gpa", required=True, type=float)
add.add_argument("--status", type=str, default="active")

view_students = subparser.add_parser("list")
view_students.add_argument("--status", type=str)

students_in_major = subparser.add_parser("find-major")
students_in_major.add_argument("--major", required=True, type=str)

update_gpa = subparser.add_parser("update-gpa")
update_gpa.add_argument("--id", required=True, type=int)
update_gpa.add_argument("--gpa", required=True, type=float)

delete = subparser.add_parser("delete")
delete.add_argument("--id", required=True, type=int)

args = parser.parse_args()
console = Console()

if args.command == "init_db":
    init_db()

elif args.command == "add":
    student_id = add_student(
        args.name,
        args.email,
        args.major,
        args.gpa,
        args.status
    )
    print(f"Student {args.name} added with ID {student_id}")

elif args.command == "update-gpa":
    rowcount = update_student_gpa(args.id, args.gpa)
    print(f"Deleted student with ID: {args.id}\n ({rowcount} rows affected)")

elif args.command == "delete":
    rowcount = delete_student(args.id)
    print(f"Updated GPA for student ID {args.id}\n ({rowcount} rows affected)")


elif args.command == "list":
    try:
        students = list_students(args.status)

        if not students:
            console.print("No students found.", style="yellow")
        else:
            table = Table(title="Students")

            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Name")
            table.add_column("Email")
            table.add_column("Major")
            table.add_column("GPA", justify="right")
            table.add_column("Status")
            table.add_column("Last Updated")

            for s in students:
                table.add_row(
                    str(s["id"]),
                    s["name"],
                    s["email"],
                    s["major"],
                    f"{s['gpa']:.1f}",
                    s["status"],
                    s["last_updated"] or "-"
                )

            console.print(table)

    except ValueError as e:
        console.print(str(e), style="red")

elif args.command == "find-major":
    students = find_students_in_major(args.major)

    if not students:
        console.print(
            f"No students found in major '{args.major}'", style="yellow")
    else:
        table = Table(title=f"Students in {args.major}")

        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name")
        table.add_column("Email")
        table.add_column("GPA", justify="right")
        table.add_column("Status")

        for s in students:
            table.add_row(
                str(s["id"]),
                s["name"],
                s["email"],
                f"{s['gpa']:.1f}",
                s["status"]
            )

        console.print(table)


# python3 success_tracker.py init_db
# python3 success_tracker.py add --name Haya --email haya@gmail.com --major cs --gpa 3.6
# python3 success_tracker.py add --name Ali --email ali@gmail.com --major cis --gpa 3.2 --status probation
# python3 success_tracker.py add --name Muna --email muna@gmail.com --major cis --gpa 2.8
# python3 success_tracker.py add --name Muna --email munagmail.com --major cis --gpa 2.8

# python3 success_tracker.py list

# python3 success_tracker.py update-gpa --id 2 --gpa 3.5
# python3 success_tracker.py update-gpa --id 2 --gpa 5

# python3 success_tracker.py list

# python3 success_tracker.py find-major --major cis
# python3 success_tracker.py find-major --major physics

# python3 success_tracker.py delete --id 3

# decorators + main 









