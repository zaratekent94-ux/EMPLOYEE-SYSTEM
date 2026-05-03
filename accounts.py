# accounts.py
# =========================
# USER ACCOUNTS (Inheritance & Polymorphism)
# =========================

from data import data_manager, notification_service
from models import UserModel, LeaveRequestModel
from datetime import datetime
from abc import ABC, abstractmethod


class BaseUser(ABC):
    """
    BaseUser abstract class - demonstrates ABSTRACTION
    Defines the interface that all user types must implement
    """
    
    def __init__(self, username: str):
        self._username = username
        self._data_manager = data_manager
    
    @property
    def username(self) -> str:
        return self._username
    
    @abstractmethod
    def get_profile(self):
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_role(self) -> str:
        """Abstract method - must be implemented by subclasses"""
        pass


class User(BaseUser):
    """
    User class - demonstrates INHERITANCE
    Inherits from BaseUser and implements its abstract methods
    """
    
    def __init__(self, username: str):
        super().__init__(username)
        self._user_model = self._data_manager.get_user_by_username(username)
    
    def get_role(self) -> str:
        """Get user role - POLYMORPHISM implementation"""
        return self._user_model.role if self._user_model else "user"
    
    def get_profile(self):
        """Get user profile"""
        if self._user_model:
            return {
                "username": self._user_model.username,
                "name": self._user_model.name,
                "dept": self._user_model.dept,
                "position": self._user_model.position,
                "phone": self._user_model.phone,
                "email": self._user_model.email,
                "leave_credits": self._user_model.leave_credits
            }
        return None
    
    @staticmethod
    def login(username: str, password: str) -> str:
        """Static method for authentication - POLYMORPHISM"""
        return data_manager.authenticate_user(username, password)


class Employee(User):
    """
    Employee class - demonstrates INHERITANCE
    Inherits from User, adds employee-specific functionality
    """
    
    def __init__(self, username: str):
        super().__init__(username)
    
    def get_role(self) -> str:
        """Override get_role - POLYMORPHISM"""
        return "user"
    
    def submit_leave(self, data: dict) -> bool:
        """Submit leave request"""
        leave_id = self._data_manager.get_next_leave_id()
        
        leave_request = LeaveRequestModel(
            leave_id=leave_id,
            username=self._username,
            leave_type=data.get("type"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            reason=data.get("reason"),
            status="Pending",
            comment="",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            seen=False
        )
        
        success = self._data_manager.add_leave_request(leave_request)
        
        # Notify admin of new leave request
        if success:
            admins = self._data_manager.get_users_by_role("admin")
            for admin in admins:
                notification_service.notify_new_leave_request(
                    admin.username, self._username, leave_id, data.get("type")
                )
        
        return success
    
    def get_my_leave(self) -> list:
        """Get user's leave requests"""
        leaves = self._data_manager.get_leave_requests_by_username(self._username)
        return [
            {
                "id": leave.leave_id,
                "type": leave.leave_type,
                "status": leave.status,
                "comment": leave.comment,
                "dates": leave.get_date_range(),
                "reason": leave.reason
            }
            for leave in leaves
        ]
    
    def get_leave_credits(self) -> int:
        """Get leave credits"""
        return self._data_manager.get_leave_credits(self._username)


class Admin(User):
    """
    Admin class - demonstrates INHERITANCE
    Inherits from User, adds admin-specific functionality
    """
    
    def __init__(self, username: str):
        super().__init__(username)
    
    def get_role(self) -> str:
        """Override get_role - POLYMORPHISM"""
        return "admin"
    
    def create_employee(self, data: dict) -> bool:
        """Create new employee - demonstrates ABSTRACTION"""
        # Check if username already exists
        if self._data_manager.get_user_by_username(data.get("username")):
            return False
        
        new_user = UserModel(
            username=data.get("username"),
            password=data.get("password", "password123"),
            role="user",
            name=data.get("name"),
            dept=data.get("dept"),
            position=data.get("position"),
            phone=data.get("phone"),
            leave_credits=15,
            email=data.get("email", "")
        )
        
        return self._data_manager.add_user(new_user)
    
    def update_employee(self, data: dict) -> bool:
        """Update employee - demonstrates ABSTRACTION"""
        username = data.get("username")
        
        update_data = {}
        if data.get("name"):
            update_data["name"] = data.get("name")
        if data.get("dept"):
            update_data["dept"] = data.get("dept")
        if data.get("position"):
            update_data["position"] = data.get("position")
        if data.get("phone"):
            update_data["phone"] = data.get("phone")
        if data.get("email"):
            update_data["email"] = data.get("email")
        if data.get("password"):
            update_data["password"] = data.get("password")
        
        return self._data_manager.update_user(username, **update_data)
    
    def delete_employee(self, username: str) -> bool:
        """Delete employee - demonstrates ABSTRACTION"""
        return self._data_manager.delete_user(username)
    
    def get_employees(self) -> list:
        """Get all employees"""
        employees = self._data_manager.get_users_by_role("user")
        return [
            {
                "username": emp.username,
                "name": emp.name,
                "dept": emp.dept,
                "position": emp.position,
                "phone": emp.phone,
                "email": emp.email
            }
            for emp in employees
        ]
    
    def get_all_leaves(self) -> list:
        """Get all leave requests"""
        leaves = self._data_manager.get_all_leave_requests()
        return [
            {
                "id": leave.leave_id,
                "username": leave.username,
                "type": leave.leave_type,
                "status": leave.status,
                "comment": leave.comment,
                "dates": leave.get_date_range(),
                "reason": leave.reason
            }
            for leave in leaves
        ]
    
    def update_leave_status(self, leave_id: int, status: str, comment: str = "") -> bool:
        """Update leave request status"""
        return self._data_manager.update_leave_request(
            leave_id,
            status=status,
            comment=comment
        )