from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from accounts import User, Admin, Employee
from data import leave_requests, users, leave_credit_history

app = Flask(__name__)
app.secret_key = "secret123"


# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    role = User.login(username, password)

    if role in ["admin", "user"]:
        session["username"] = username
        session["role"] = role
        
        if role == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
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
        return redirect(url_for("login_page"))
    return render_template("admin_dashboard.html")


@app.route("/create_employee", methods=["POST"])
def create_employee():
    if session.get("role") != "admin":
        return redirect(url_for("login_page"))
    
    admin = Admin(session["username"])
    admin.create_employee(request.form)
    return redirect(url_for("admin_dashboard"))


@app.route("/update_employee", methods=["POST"])
def update_employee():
    if session.get("role") != "admin":
        return redirect(url_for("login_page"))
    
    admin = Admin(session["username"])
    admin.update_employee(request.form)
    return redirect(url_for("admin_dashboard"))


@app.route("/get_employees")
def get_employees():
    if session.get("role") != "admin":
        return jsonify([]), 403
    
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
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

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
    if session.get("role") != "user":
        return redirect(url_for("login_page"))

    emp = Employee(session["username"])
    user_data = emp.get_profile()
    
    if user_data:
        user = user_data[0]
        
        # Get leave credits
        credits = 15
        for u in users:
            if u["username"] == session["username"]:
                credits = u.get("leave_credits", 15)
                break
        
        return render_template(
            "user_dashboard.html", 
            user=user, 
            credits=credits,
            username=user[0],
            name=user[1],
            dept=user[2],
            position=user[3],
            phone=user[4]
        )
    
    return redirect(url_for("login_page"))


# =========================
# LEAVE ROUTES
# =========================

@app.route("/submit_leave", methods=["POST"])
def submit_leave():
    if "username" not in session:
        return redirect(url_for("login_page"))

    leave_type = request.form.get("type")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    reason = request.form.get("reason")

    if not leave_type or not start_date or not end_date or not reason:
        return redirect(url_for("user_dashboard"))

    emp = Employee(session["username"])
    emp.submit_leave({
        "type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason
    })

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


@app.route("/get_leave_credits")
def get_leave_credits():
    if "username" not in session:
        return jsonify({"credits": 0, "history": []})
    
    username = session["username"]
    
    for user in users:
        if user["username"] == username:
            return jsonify({
                "credits": user.get("leave_credits", 15),
                "history": leave_credit_history.get(username, [])
            })
    
    return jsonify({"credits": 0, "history": []})


@app.route("/update_leave_status", methods=["POST"])
def update_leave_status():
    global leave_credit_history
    
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    leave_id = data.get("id")
    status = data.get("status")
    comment = data.get("comment", "")

    admin = Admin(session["username"])
    admin.update_leave_status(leave_id, status, comment)

    # If approved, deduct leave credits
    if status == "Approved":
        for leave in leave_requests:
            if leave["id"] == leave_id:
                username = leave["username"]
                
                from datetime import datetime
                start = datetime.strptime(leave["start_date"], "%Y-%m-%d")
                end = datetime.strptime(leave["end_date"], "%Y-%m-%d")
                days = (end - start).days + 1
                
                for user in users:
                    if user["username"] == username:
                        current_credits = user.get("leave_credits", 15)
                        user["leave_credits"] = current_credits - days
                        
                        if username not in leave_credit_history:
                            leave_credit_history[username] = []
                        
                        leave_credit_history[username].append({
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "action": "Deducted",
                            "amount": days,
                            "balance": user["leave_credits"],
                            "reason": f"Leave ID {leave_id}"
                        })
                        break
                break

    return jsonify({"message": f"{status} successfully"})


@app.route("/get_notifications")
def get_notifications():
    if "username" not in session:
        return jsonify([])

    username = session["username"]
    user_notifications = []

    for l in leave_requests:
        if l["username"] == username and l.get("status") in ["Approved", "Rejected"]:
            user_notifications.append({
                "id": l["id"],
                "type": l.get("type", ""),
                "status": l["status"],
                "start_date": l.get("start_date", ""),
                "end_date": l.get("end_date", ""),
                "comment": l.get("comment", ""),
                "seen": l.get("seen", False)
            })

    # Mark as seen
    for l in leave_requests:
        if l["username"] == username:
            l["seen"] = True

    # Reverse to show newest first
    user_notifications.reverse()
    
    return jsonify(user_notifications)


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)