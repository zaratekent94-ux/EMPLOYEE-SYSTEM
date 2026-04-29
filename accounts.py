# accounts.py

from flask import session
from data import users, leave_requests
from datetime import datetime

class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def login(username, password):
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user["role"]
        return None


class Admin(User):

    def create_employee(self, data):
        for user in users:
            if user["username"] == data.get("username"):
                return False

        users.append({
            "username": data.get("username"),
            "password": data.get("password", "password123"),
            "role": "user",
            "name": data.get("name"),
            "dept": data.get("dept"),
            "position": data.get("position"),
            "phone": data.get("phone"),
            "leave_credits": 15
        })
        return True

    def update_employee(self, data):
        username = data.get("username")
        for user in users:
            if user["username"] == username:
                if data.get("name"):
                    user["name"] = data.get("name")
                if data.get("dept"):
                    user["dept"] = data.get("dept")
                if data.get("position"):
                    user["position"] = data.get("position")
                if data.get("phone"):
                    user["phone"] = data.get("phone")
                if data.get("password"):
                    user["password"] = data.get("password")
                return True
        return False

    def delete_employee(self, username):
        global users
        users[:] = [u for u in users if u["username"] != username]
        return True

    def get_employees(self):
        return [
            (u["username"], u["name"], u["dept"], u["position"], u["phone"])
            for u in users if u["role"] == "user"
        ]

    def get_all_leaves(self):
        return [
            (
                i, 
                l["username"], 
                l.get("type", ""), 
                l["status"], 
                l.get("comment", ""),
                f"{l.get('start_date', '')} to {l.get('end_date', '')}",
                l.get("reason", "")
            )
            for i, l in enumerate(leave_requests)
        ]

    def update_leave_status(self, leave_id, status, comment=""):
        # Find and update the leave request
        for leave in leave_requests:
            if leave["id"] == leave_id:
                leave["status"] = status
                leave["comment"] = comment
                leave["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                return True
        return False


class Employee(User):

    def get_profile(self):
        for user in users:
            if user["username"] == self.username:
                return [(user["username"], user["name"], user["dept"], user["position"], user["phone"])]
        return None

    def submit_leave(self, data):
        leave_id = len(leave_requests) + 1
        
        leave_requests.append({
            "id": leave_id,
            "username": self.username,
            "type": data.get("type"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "reason": data.get("reason"),
            "status": "Pending",
            "comment": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "seen": False
        })
        return True

    def get_my_leave(self):
        return [
            {
                "id": l["id"],
                "type": l.get("type", ""),
                "status": l["status"],
                "comment": l.get("comment", ""),
                "dates": f"{l.get('start_date', '')} to {l.get('end_date', '')}",
                "reason": l.get("reason", "")
            }
            for l in leave_requests if l["username"] == self.username
        ]