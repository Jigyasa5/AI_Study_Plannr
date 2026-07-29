from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session, flash
from gemini_ai import generate_plan as ai_generate_plan
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "studyplanner"

def init_db():
    print("Creating database tables...")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_name TEXT,
        deadline TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT,
        exam_date TEXT,
        hours TEXT,
        plan TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")
    init_db()

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(name, email, password) VALUES(?,?,?)",
                (name, email, password)
            )

            conn.commit()

            flash("Registration Successful! Please login.", "success")
            return redirect("/login")

        except sqlite3.IntegrityError:
            flash("Email already registered. Please login.", "danger")
            return redirect("/signup")

        finally:
            conn.close()

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?", (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]      # store user ID
            session["user_name"] = user[1]    # store user name
            return redirect("/dashboard")

        flash("Invalid Email or Password","danger")
        return redirect("/login")
    
    

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    user_id = session["user_id"]

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (user_id,)
    )

    tasks = cursor.fetchall()

    total = len(tasks)
    completed = sum(1 for task in tasks if task[4] == "Completed")
    pending = total - completed

    progress = 0
    if total > 0:
     progress = int((completed / total) * 100)

    conn.close()

    return render_template(
    "dashboard.html",
    name=session["user_name"],
    tasks=tasks,
    total=total,
    completed=completed,
    pending=pending,
    progress=progress
)

## Add Task
@app.route("/add_task", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return redirect("/login")

    task = request.form["task"]
    deadline = request.form["deadline"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(user_id, task_name, deadline, status) VALUES(?,?,?,?)",
        (session["user_id"], task, deadline, "Pending")
    )

    conn.commit()
    conn.close()          # Make sure this line exists!

    return redirect("/dashboard")

## Delete Task
@app.route("/delete_task/<int:id>")
def delete_task(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

## Complete Task
@app.route("/complete_task/<int:id>")
def complete_task(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

#---------------- STUDY PLANNER ----------------
@app.route("/study_planner")
def study_planner():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("study_planner.html")


# ---------------- Generate AI Plan ----------------
@app.route("/generate_ai_plan", methods=["POST"])
def generate_ai_plan():

    if "user_id" not in session:
        return redirect("/login")

    subject = request.form["subject"]
    exam_date = request.form["exam_date"]
    hours = request.form["hours"]
    difficulty = request.form["difficulty"]

    plan = ai_generate_plan(
        subject,
        exam_date,
        hours,
        difficulty
    )

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(""" 
    INSERT INTO study_plans(user_id, subject, exam_date, hours, plan)
    VALUES (?, ?, ?, ?, ?)
    """, (
    session["user_id"],
    subject,
    exam_date,
    hours,
    plan
    ))

    conn.commit()
    conn.close()

    return render_template(
        "generate_plan.html",
        plan=plan
    )

#---------------- View Plan ----------------
@app.route("/view_plan")
def view_plan():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT subject, exam_date, hours
        FROM study_plans
        WHERE user_id=?
        """,
        (session["user_id"],)
    )

    plans = cursor.fetchall()

    conn.close()

    return render_template(
        "view_plan.html",
        plans=plans
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user_id", None)
    session.pop("user_name", None)

    flash("Logged Out Successfully","success")
    return redirect("/login")



if __name__ == "__main__":
    
    app.run(debug=True)