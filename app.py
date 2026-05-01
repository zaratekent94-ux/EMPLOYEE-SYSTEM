# app.py
# =========================
# FLASK APPLICATION (OOP Structure)
# =========================

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
from accounts import User, Admin, Employee
from data import data_manager, notification_service
from datetime import datetime
import io

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
    
    user = data_manager.get_user_by_username(username)
    if user:
        return jsonify(user.to_dict())
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
        credits = emp.get_leave_credits()
        
        return render_template(
            "user_dashboard.html", 
            user=(user_data["username"], user_data["name"], user_data["dept"], 
                  user_data["position"], user_data["phone"]),
            credits=credits,
            username=user_data["username"],
            name=user_data["name"],
            dept=user_data["dept"],
            position=user_data["position"],
            phone=user_data["phone"]
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
    credits = data_manager.get_leave_credits(username)
    history = data_manager.get_leave_credit_history(username)
    
    return jsonify({
        "credits": credits,
        "history": history
    })


@app.route("/update_leave_status", methods=["POST"])
def update_leave_status():
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
        leave = data_manager.get_leave_request_by_id(leave_id)
        if leave:
            username = leave.username
            
            start = datetime.strptime(leave.start_date, "%Y-%m-%d")
            end = datetime.strptime(leave.end_date, "%Y-%m-%d")
            days = (end - start).days + 1
            
            current_credits = data_manager.get_leave_credits(username)
            new_credits = current_credits - days
            
            data_manager.update_leave_credits(username, new_credits)
            data_manager.add_leave_credit_history(
                username, "Deducted", days, new_credits, f"Leave ID {leave_id}"
            )

    # Send notification to user about status change
    if status in ["Approved", "Rejected"]:
        leave = data_manager.get_leave_request_by_id(leave_id)
        if leave:
            notification_service.notify_leave_status_change(
                leave.username, leave_id, status, comment
            )

    return jsonify({"message": f"{status} successfully"})


@app.route("/get_notifications")
def get_notifications():
    if "username" not in session:
        return jsonify([])

    username = session["username"]
    leaves = data_manager.get_leave_requests_by_username(username)
    
    user_notifications = [
        {
            "id": leave.leave_id,
            "type": leave.leave_type,
            "status": leave.status,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "comment": leave.comment,
            "seen": leave.seen
        }
        for leave in leaves
        if leave.status in ["Approved", "Rejected"]
    ]

    # Mark all as seen
    for leave in leaves:
        if leave.status in ["Approved", "Rejected"]:
            data_manager.update_leave_request(leave.leave_id, seen=True)

    # Reverse to show newest first
    user_notifications.reverse()
    
    return jsonify(user_notifications)


# =========================
# NOTIFICATION ROUTES
# =========================

@app.route("/get_app_notifications")
def get_app_notifications():
    """Get in-app notifications for current user"""
    if "username" not in session:
        return jsonify([]), 403
    
    username = session["username"]
    unread_only = request.args.get("unread_only", "false").lower() == "true"
    
    notifications = notification_service.get_notifications(username, unread_only)
    return jsonify(notifications)


@app.route("/get_unread_notification_count")
def get_unread_notification_count():
    """Get count of unread notifications"""
    if "username" not in session:
        return jsonify({"count": 0})
    
    username = session["username"]
    count = notification_service.get_unread_count(username)
    
    return jsonify({"count": count})


@app.route("/mark_notification_read", methods=["POST"])
def mark_notification_read():
    """Mark a notification as read"""
    if "username" not in session:
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    notification_id = data.get("notification_id")
    
    if not notification_id:
        return jsonify({"message": "Invalid notification ID"}), 400
    
    username = session["username"]
    success = notification_service.mark_as_read(username, notification_id)
    
    if success:
        return jsonify({"message": "Notification marked as read"})
    return jsonify({"message": "Notification not found"}), 404


@app.route("/mark_all_notifications_read", methods=["POST"])
def mark_all_notifications_read():
    """Mark all notifications as read"""
    if "username" not in session:
        return jsonify({"message": "Unauthorized"}), 403
    
    username = session["username"]
    count = notification_service.mark_all_as_read(username)
    
    return jsonify({"message": f"{count} notifications marked as read"})


@app.route("/send_email_notification", methods=["POST"])
def send_email_notification():
    """Send email notification (admin only)"""
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    email = data.get("email")
    subject = data.get("subject")
    body = data.get("body")
    
    if not email or not subject or not body:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check for spam - simple rate limiting
    # In production, implement proper rate limiting
    result = notification_service.send_email_notification(email, subject, body)
    
    return jsonify(result)


@app.route("/send_sms_notification", methods=["POST"])
def send_sms_notification():
    """Send SMS notification (admin only)"""
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    phone = data.get("phone")
    message = data.get("message")
    
    if not phone or not message:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check for spam - message length and content validation
    if len(message) > 500:
        return jsonify({"message": "Message too long (max 500 characters)"}), 400
    
    # Basic spam check - reject if message contains too many URLs
    url_count = message.lower().count("http")
    if url_count > 2:
        return jsonify({"message": "Message flagged as potential spam"}), 400
    
    result = notification_service.send_sms_notification(phone, message)
    
    return jsonify(result)


# =========================
# REPORT & EXPORT ROUTES
# =========================

@app.route("/generate_employee_report")
def generate_employee_report():
    """Generate employee report data"""
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    employees = data_manager.get_users_by_role("user")
    report_data = {
        "title": "Employee Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_employees": len(employees),
        "employees": [
            {
                "username": emp.username,
                "name": emp.name,
                "department": emp.dept,
                "position": emp.position,
                "phone": emp.phone,
                "leave_credits": emp.leave_credits
            }
            for emp in employees
        ]
    }
    return jsonify(report_data)


@app.route("/generate_leave_report")
def generate_leave_report():
    """Generate leave report data"""
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    leaves = data_manager.get_all_leave_requests()
    report_data = {
        "title": "Leave Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_requests": len(leaves),
        "pending": len([l for l in leaves if l.status == "Pending"]),
        "approved": len([l for l in leaves if l.status == "Approved"]),
        "rejected": len([l for l in leaves if l.status == "Rejected"]),
        "leaves": [
            {
                "id": l.leave_id,
                "username": l.username,
                "type": l.leave_type,
                "start_date": l.start_date,
                "end_date": l.end_date,
                "reason": l.reason,
                "status": l.status,
                "comment": l.comment,
                "created_at": l.created_at
            }
            for l in leaves
        ]
    }
    return jsonify(report_data)


@app.route("/export_employees/<format>")
def export_employees(format):
    """Export employees to PDF or Excel"""
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    employees = data_manager.get_users_by_role("user")
    
    if format == "excel":
        # Create CSV content
        output = io.StringIO()
        output.write("Username,Name,Department,Position,Phone,Leave Credits\n")
        for emp in employees:
            output.write(f"{emp.username},{emp.name},{emp.dept},{emp.position},{emp.phone},{emp.leave_credits}\n")
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"employee_report_{datetime.now().strftime('%Y%m%d')}.csv"
        )
    
    elif format == "pdf":
        # Create simple text report for PDF
        output = io.StringIO()
        output.write("=" * 60 + "\n")
        output.write("EMPLOYEE REPORT\n")
        output.write("=" * 60 + "\n")
        output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.write(f"Total Employees: {len(employees)}\n")
        output.write("=" * 60 + "\n\n")
        
        for emp in employees:
            output.write(f"Username: {emp.username}\n")
            output.write(f"Name: {emp.name}\n")
            output.write(f"Department: {emp.dept}\n")
            output.write(f"Position: {emp.position}\n")
            output.write(f"Phone: {emp.phone}\n")
            output.write(f"Leave Credits: {emp.leave_credits}\n")
            output.write("-" * 40 + "\n")
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype="text/plain",
            as_attachment=True,
            download_name=f"employee_report_{datetime.now().strftime('%Y%m%d')}.txt"
        )
    
    return jsonify({"message": "Invalid format"}), 400


@app.route("/export_leaves/<format>")
def export_leaves(format):
    """Export leaves to PDF or Excel"""
    if session.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403
    
    leaves = data_manager.get_all_leave_requests()
    
    if format == "excel":
        output = io.StringIO()
        output.write("ID,Employee,Type,Start Date,End Date,Reason,Status,Comment,Created At\n")
        for l in leaves:
            output.write(f'{l.leave_id},{l.username},{l.leave_type},{l.start_date},{l.end_date},"{l.reason}",{l.status},"{l.comment}",{l.created_at}\n')
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"leave_report_{datetime.now().strftime('%Y%m%d')}.csv"
        )
    
    elif format == "pdf":
        output = io.StringIO()
        output.write("=" * 60 + "\n")
        output.write("LEAVE REPORT\n")
        output.write("=" * 60 + "\n")
        output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output.write(f"Total Requests: {len(leaves)}\n")
        output.write(f"Pending: {len([l for l in leaves if l.status == 'Pending'])}\n")
        output.write(f"Approved: {len([l for l in leaves if l.status == 'Approved'])}\n")
        output.write(f"Rejected: {len([l for l in leaves if l.status == 'Rejected'])}\n")
        output.write("=" * 60 + "\n\n")
        
        for l in leaves:
            output.write(f"ID: {l.leave_id}\n")
            output.write(f"Employee: {l.username}\n")
            output.write(f"Type: {l.leave_type}\n")
            output.write(f"Dates: {l.start_date} to {l.end_date}\n")
            output.write(f"Reason: {l.reason}\n")
            output.write(f"Status: {l.status}\n")
            output.write(f"Comment: {l.comment}\n")
            output.write(f"Created: {l.created_at}\n")
            output.write("-" * 40 + "\n")
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype="text/plain",
            as_attachment=True,
            download_name=f"leave_report_{datetime.now().strftime('%Y%m%d')}.txt"
        )
    
    return jsonify({"message": "Invalid format"}), 400


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)