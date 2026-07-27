# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin
# from flask_login import login_user, logout_user
# from flask_login import login_required, current_user

# app = Flask(__name__)

# app.config['SECRET_KEY'] = 'secret123'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyplanner.db'

# db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

# # ---------------- USER TABLE ----------------

# class User(UserMixin, db.Model):

#     id = db.Column(db.Integer, primary_key=True)

#     username = db.Column(db.String(100))

#     password = db.Column(db.String(100))

# # ---------------- STUDY TASK TABLE ----------------

# class StudyTask(db.Model):

#     id = db.Column(db.Integer, primary_key=True)

#     subject = db.Column(db.String(100))

#     hours = db.Column(db.Integer)

#     user_id = db.Column(db.Integer)

# # ---------------- LOGIN ----------------

# @login_manager.user_loader
# def load_user(user_id):

#     return User.query.get(int(user_id))

# # ---------------- HOME ----------------

# @app.route('/')
# def home():

#     return render_template('index.html')

# # ---------------- REGISTER ----------------

# @app.route('/register', methods=['GET', 'POST'])
# def register():

#     if request.method == 'POST':

#         username = request.form['username']

#         password = request.form['password']
 
#         user = User(
#             username=username,
#             password=password
#         )

#         db.session.add(user)

#         db.session.commit()

#         return redirect('/login')

#     return render_template('register.html')

# # ---------------- LOGIN ----------------

# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     if request.method == 'POST':

#         username = request.form['username']

#         password = request.form['password']

#         user = User.query.filter_by(
#             username=username,
#             password=password
#         ).first()

#         if user:

#             login_user(user)

#             return redirect('/dashboard')

#     return render_template('login.html')

# # ---------------- DASHBOARD ----------------

# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():

#     if request.method == 'POST':

#         subject = request.form['subject']

#         hours = request.form['hours']

#         task = StudyTask(
#             subject=subject,
#             hours=hours,
#             user_id=current_user.id
#         )

#         db.session.add(task)

#         db.session.commit()

#     tasks = StudyTask.query.filter_by(
#         user_id=current_user.id
#     ).all()

#     # AI Logic
#     ai_plan = []

#     for task in tasks:

#         if int(task.hours) >= 3:

#             ai_plan.append(
#                 f"High Priority: {task.subject}"
#             )

#         else:

#             ai_plan.append(
#                 f"Normal Priority: {task.subject}"
#             )

#     return render_template(
#         'dashboard.html',
#         tasks=tasks,
#         ai_plan=ai_plan
#     )

# # ---------------- LOGOUT ----------------

# @app.route('/logout')
# @login_required
# def logout():

#     logout_user()

#     return redirect('/')

# # ---------------- RUN ----------------

# if __name__ == '__main__':

#     with app.app_context():

#         db.create_all()

#     app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)