from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# -----------------------------------
# DATABASE SETUP
# -----------------------------------
def init_db():
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        name TEXT,
        dept TEXT,
        position TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------------
# DEFAULT ADMIN
# -----------------------------------
def create_default_admin():
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    admin_exists = c.fetchone()

    if not admin_exists:
        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("admin", "password123", "admin"))

        conn.commit()

    conn.close()

create_default_admin()

# -----------------------------------
# BASE CLASS
# -----------------------------------
class User:
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role

# -----------------------------------
# EMPLOYEE CLASS
# -----------------------------------
class Employee(User):
    def __init__(self, username, password):
        super().__init__(username, password, "user")

    def dashboard(self):
        return "user_dashboard"

# -----------------------------------
# ADMIN CLASS
# -----------------------------------
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def dashboard(self):
        return "admin_dashboard"

    def create_employee(self, username, password, name, dept, position, phone):
        conn = sqlite3.connect("employees.db")
        c = conn.cursor()

        try:
            c.execute("""
            INSERT INTO users (username, password, role, name, dept, position, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, password, "user", name, dept, position, phone))

            conn.commit()
            conn.close()
            return "Employee account created successfully"

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

        except Exception as e:
            conn.close()
            print("DATABASE ERROR:", e)
            return "Database error"

# -----------------------------------
# LOGIN FUNCTION
# -----------------------------------
def get_user(username, password):
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    c.execute("""
        SELECT username, password, role 
        FROM users 
        WHERE username=? AND password=?
    """, (username, password))

    data = c.fetchone()
    conn.close()

    if data:
        session["username"] = data[0]
        session["role"] = data[2]

        if data[2] == "admin":
            return Admin(data[0], data[1])
        else:
            return Employee(data[0], data[1])

    return None

# -----------------------------------
# ROUTES
# -----------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = get_user(username, password)

    if user:
        return redirect(url_for(user.dashboard()))
    else:
        return render_template("login.html", message="Invalid login")

# -----------------------------------
# LOGOUT
# -----------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# -----------------------------------
# CREATE EMPLOYEE
# -----------------------------------
@app.route("/create_employee", methods=["POST"])
def create_employee_route():
    if session.get("role") != "admin":
        return redirect(url_for("index"))

    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    dept = request.form.get("dept")
    position = request.form.get("position")
    phone = request.form.get("phone")

    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    try:
        c.execute("""
        INSERT INTO users (username, password, role, name, dept, position, phone)
        VALUES (?, ?, 'user', ?, ?, ?, ?)
        """, (username, password, name, dept, position, phone))

        conn.commit()

    except Exception as e:
        print("CREATE ERROR:", e)

    conn.close()

    return redirect(url_for("admin_dashboard"))

# -----------------------------------
# GET EMPLOYEES (FIXED)
# -----------------------------------
@app.route("/get_employees")
def get_employees():
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    c.execute("""
        SELECT username, name, dept, position, phone 
        FROM users 
        WHERE role='user'
    """)

    data = c.fetchall()
    conn.close()

    return jsonify(data)

# -----------------------------------
# DELETE EMPLOYEE (ADDED)
# -----------------------------------
@app.route("/delete_employee", methods=["POST"])
def delete_employee():
    if session.get("role") != "admin":
        return "Unauthorized", 403

    data = request.get_json()
    username = data.get("username")

    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    try:
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()

    except Exception as e:
        print("DELETE ERROR:", e)
        return "Server error", 500

    conn.close()

    return "Deleted", 200

# -----------------------------------
# DASHBOARDS
# -----------------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("index"))
    return render_template("admin_dashboard.html")

@app.route("/user_dashboard")
def user_dashboard():
    if "username" not in session:
        return redirect(url_for("index"))

    conn = sqlite3.connect("employees.db")
    c = conn.cursor()

    c.execute("""
        SELECT username, name, dept, position, phone
        FROM users
        WHERE username=?
    """, (session["username"],))

    data = c.fetchone()
    conn.close()

    return render_template("user_dashboard.html", user=data)

# -----------------------------------
# RUN
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)