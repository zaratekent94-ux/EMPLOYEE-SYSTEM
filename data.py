# data.py

# =========================
# STORAGE (NO DATABASE)
# =========================

# Initialize leave_requests as global
leave_requests = []

# Leave credit history tracking
leave_credit_history = {}  # {username: [{date, action, amount, balance, reason}]}

# Users with leave credits
users = [
    {
        "username": "admin",
        "password": "admin123",
        "role": "admin",  # ← MUST BE "admin"
        "name": "Administrator",
        "dept": "IT",
        "position": "System Admin",
        "phone": "+1234567890",
        "leave_credits": 0  # Admin doesn't need leave
    },
    {
        "username": "john",
        "password": "john123",
        "role": "user",
        "name": "John Doe",
        "dept": "Engineering",
        "position": "Software Engineer",
        "phone": "+1987654321",
        "leave_credits": 15  # 15 days per year
    },
    {
        "username": "jane",
        "password": "jane123",
        "role": "user",
        "name": "Jane Smith",
        "dept": "Human Resources",
        "position": "HR Manager",
        "phone": "+1123456789",
        "leave_credits": 15
    }
]