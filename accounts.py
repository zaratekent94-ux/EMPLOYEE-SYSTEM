# accounts.py

from flask import session
from data import users, leave_requests   # ← IMPORT HERE


class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def login(username, password):
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"] = user["username"]
                session["role"] = user["role"]
                return user["role"]
        return None


class Admin(User):

    def create_employee(self, data):
        for user in users:
            if user["username"] == data["username"]:
                return False

        users.append({
            "username": data["username"],
            "password": data["password"],
            "role": "user",
            "name": data["name"],
            "dept": data["dept"],
            "position": data["position"],
            "phone": data["phone"]
        })
        return True

    def update_employee(self, data):
        for user in users:
            if user["username"] == data["username"]:
                user["name"] = data["name"]
                user["dept"] = data["dept"]
                user["position"] = data["position"]
                user["phone"] = data["phone"]

    def delete_employee(self, username):
        users[:] = [u for u in users if u["username"] != username]  # safer update

    def get_employees(self):
        return [
            (u["username"], u["name"], u["dept"], u["position"], u["phone"])
            for u in users if u["role"] == "user"
        ]

    def get_all_leaves(self):
        return [
            (i, l["username"], l["reason"], l["status"], l.get("comment", ""))
            for i, l in enumerate(leave_requests)
        ]

    def update_leave_status(self, leave_id, status, comment=""):
        if 0 <= leave_id < len(leave_requests):
            leave_requests[leave_id]["status"] = status
            leave_requests[leave_id]["comment"] = comment
            leave_requests[leave_id]["seen"] = False   # 🔔 trigger notification


class Employee(User):

    def get_profile(self):
        for user in users:
            if user["username"] == self.username:
                return [(user["username"], user["name"], user["dept"], user["position"], user["phone"])]

    def submit_leave(self, data):
        leave_requests.append({
            "username": self.username,
            "type": data.get("type", ""),
            "start_date": data.get("start_date", ""),
            "end_date": data.get("end_date", ""),
            "reason": data.get("reason", ""),
            "status": "Pending",
            "comment": "",
            "seen": False
        })

    def get_my_leave(self):
        return [
            {
                "type": l.get("type", "-"),
                "dates": f"{l.get('start_date', '')} - {l.get('end_date', '')}",
                "reason": l.get("reason", "-"),
                "status": l.get("status", "Pending"),
                "comment": l.get("comment", ""),
                "seen": l.get("seen", False)
            }
            for l in leave_requests if l["username"] == self.username
        ]