from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "studyplanner"

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

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
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]      # store user ID
            session["user_name"] = user[1]    # store user name
            return redirect("/dashboard")

        return "Invalid Email or Password"

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

    conn.close()

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        tasks=tasks
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

    user_id = session["user_id"]

    cursor.execute(
        "INSERT INTO tasks(user_id, task_name, deadline, status) VALUES(?,?,?,?)",
        (user_id, task, deadline, "Pending")
    )

    conn.commit()
    conn.close()

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

#---------------- Generate Plan ----------------
@app.route("/generate_plan", methods=["POST"])
def generate_plan():

    subject = request.form["subject"]
    exam = request.form["exam_date"]
    hours = request.form["hours"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO study_plans(user_id, subject, exam_date, hours)
        VALUES(?,?,?,?)
        """,
        (
            session["user_id"],
            subject,
            exam,
            hours
        )
    )

    conn.commit()
    conn.close()

    return redirect("/view_plan")

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

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)