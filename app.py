from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from accounts import User, Admin, Employee
from data import leave_requests, users # ← IMPORT LEAVE REQUESTS   

app = Flask(__name__)
app.secret_key = "secret123"


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
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    
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


@app.route("/get_employee/<username>")
def get_employee(username):
    if session.get("role") != "admin":
        return jsonify({}), 403
    
    for user in users:
        if user["username"] == username:
            return jsonify(user)
    return jsonify({}), 404


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
    emp.submit_leave(request.form)

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
    data = request.get_json()

    leave_id = data.get("id")
    status = data.get("status")
    comment = data.get("comment", "")   # ← IMPORTANT

    admin = Admin(session["username"])
    admin.update_leave_status(leave_id, status, comment)

    return jsonify({"message": f"{status} successfully"})


@app.route("/get_notifications")
def get_notifications():
    if "username" not in session:
        return jsonify([])

    notifications = []

    for l in leave_requests:
        if l["username"] == session["username"] and not l.get("seen", False):
            notifications.append(l)
            l["seen"] = True

    return jsonify(notifications)

# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)