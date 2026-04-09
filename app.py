from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Example users: username -> [password, role]
users = {
    "admin": ["password123", "admin"],
    "user1": ["pass1", "user"]
}

# Login page
@app.route("/", methods=["GET"])
def index():
    return render_template("login.html", message='')

# Handle login
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users:
        if users[username][0] == password:
            role = users[username][1]
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return render_template('login.html', message='Invalid password')
    else:
        return render_template('login.html', message='Invalid username')

# Admin dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template('admin_dashboard.html')

# User dashboard
@app.route("/user_dashboard")
def user_dashboard():
    return render_template('user_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)