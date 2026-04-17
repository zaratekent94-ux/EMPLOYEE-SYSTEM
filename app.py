from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# =========================
# DATABASE CLASS
# =========================
class Database:
    def __init__(self):
        self.db = "employees.db"
        self.init_db()

    def connect(self):
        return sqlite3.connect(self.db)

    def init_db(self):
        conn = self.connect()
        c = conn.cursor()

        # USERS
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

        # ✅ LEAVE TABLE (ADDED)
        c.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Pending'
        )
        """)

        conn.commit()
        conn.close()

    def execute(self, query, params=(), fetch=False):
        conn = self.connect()
        c = conn.cursor()

        c.execute(query, params)

        data = None
        if fetch:
            data = c.fetchall()

        conn.commit()
        conn.close()

        return data


db = Database()

# =========================
# USER BASE CLASS
# =========================
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def login(username, password):
        result = db.execute(
            "SELECT username, role FROM users WHERE username=? AND password=?",
            (username, password),
            fetch=True
        )

        if result:
            user = result[0]
            session["username"] = user[0]
            session["role"] = user[1]
            return user[1]

        return None


# =========================
# ADMIN CLASS
# =========================
class Admin(User):

    def create_employee(self, data):
        try:
            db.execute("""
            INSERT INTO users (username, password, role, name, dept, position, phone)
            VALUES (?, ?, 'user', ?, ?, ?, ?)
            """, (
                data["username"],
                data["password"],
                data["name"],
                data["dept"],
                data["position"],
                data["phone"]
            ))
            return True
        except:
            return False

    def update_employee(self, data):
        db.execute("""
        UPDATE users
        SET name=?, dept=?, position=?, phone=?
        WHERE username=?
        """, (
            data["name"],
            data["dept"],
            data["position"],
            data["phone"],
            data["username"]
        ))

    def delete_employee(self, username):
        db.execute("DELETE FROM users WHERE username=?", (username,))

    def get_employees(self):
        return db.execute("""
        SELECT username, name, dept, position, phone
        FROM users WHERE role='user'
        """, fetch=True)

    # ✅ LEAVE MANAGEMENT
    def get_all_leaves(self):
        return db.execute("""
        SELECT id, username, reason, status
        FROM leave_requests
        """, fetch=True)

    def update_leave_status(self, leave_id, status):
        db.execute("""
        UPDATE leave_requests
        SET status=?
        WHERE id=?
        """, (status, leave_id))


# =========================
# EMPLOYEE CLASS
# =========================
class Employee(User):

    def get_profile(self):
        return db.execute("""
        SELECT username, name, dept, position, phone
        FROM users WHERE username=?
        """, (self.username,), fetch=True)

    # ✅ SUBMIT LEAVE
    def submit_leave(self, reason):
        db.execute("""
        INSERT INTO leave_requests (username, reason)
        VALUES (?, ?)
        """, (self.username, reason))

    # ✅ GET MY LEAVE
    def get_my_leave(self):
        return db.execute("""
        SELECT reason, status
        FROM leave_requests
        WHERE username=?
        """, (self.username,), fetch=True)


# =========================
# DEFAULT ADMIN
# =========================
def create_default_admin():
    result = db.execute("SELECT * FROM users WHERE username=?", ("admin",), fetch=True)

    if not result:
        db.execute("""
        INSERT INTO users (username, password, role)
        VALUES ('admin', 'password123', 'admin')
        """)

create_default_admin()

# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    role = User.login(username, password)

    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    elif role == "user":
        return redirect(url_for("user_dashboard"))

    return render_template("login.html", message="Invalid login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# =========================
# ADMIN ROUTES
# =========================

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    return render_template("admin_dashboard.html")


@app.route("/create_employee", methods=["POST"])
def create_employee():
    admin = Admin(session["username"])
    admin.create_employee(request.form)
    return redirect(url_for("admin_dashboard"))


@app.route("/update_employee", methods=["POST"])
def update_employee():
    admin = Admin(session["username"])
    admin.update_employee(request.form)
    return redirect(url_for("admin_dashboard"))


@app.route("/get_employees")
def get_employees():
    admin = Admin(session["username"])
    data = admin.get_employees()
    return jsonify(data)


@app.route("/delete_employee", methods=["POST"])
def delete_employee():
    admin = Admin(session["username"])

    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"message": "Invalid username"}), 400

    admin.delete_employee(username)

    return jsonify({"message": "Deleted successfully"})


# =========================
# USER DASHBOARD
# =========================

@app.route("/user_dashboard")
def user_dashboard():
    if "username" not in session:
        return redirect(url_for("index"))

    emp = Employee(session["username"])
    user = emp.get_profile()[0]

    return render_template("user_dashboard.html", user=user)


# =========================
# LEAVE ROUTES
# =========================

@app.route("/submit_leave", methods=["POST"])
def submit_leave():
    if "username" not in session:
        return redirect(url_for("index"))

    emp = Employee(session["username"])
    reason = request.form.get("reason")

    emp.submit_leave(reason)

    return redirect(url_for("user_dashboard"))


@app.route("/get_my_leave")
def get_my_leave():
    if "username" not in session:
        return jsonify([])

    emp = Employee(session["username"])
    data = emp.get_my_leave()

    return jsonify(data)


@app.route("/get_all_leaves")
def get_all_leaves():
    if session.get("role") != "admin":
        return jsonify([])

    admin = Admin(session["username"])
    data = admin.get_all_leaves()

    return jsonify(data)


@app.route("/update_leave_status", methods=["POST"])
def update_leave_status():
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    leave_id = data.get("id")
    status = data.get("status")

    admin = Admin(session["username"])
    admin.update_leave_status(leave_id, status)

    return jsonify({"message": f"{status} successfully"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)