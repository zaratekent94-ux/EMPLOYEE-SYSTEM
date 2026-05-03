# models.py
# =========================
# DATA MODELS (Encapsulation)
# =========================

from datetime import datetime
from typing import Optional, List, Dict, Any


class UserModel:
    """Base user model with encapsulated data"""
    
    def __init__(self, username: str, password: str, role: str, name: str = "", 
                 dept: str = "", position: str = "", phone: str = "", leave_credits: int = 15, email: str = ""):
        self._username = username
        self._password = password
        self._role = role
        self._name = name
        self._dept = dept
        self._position = position
        self._phone = phone
        self._leave_credits = leave_credits
        self._email = email
    
    # Getters (Encapsulation)
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def role(self) -> str:
        return self._role
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def dept(self) -> str:
        return self._dept
    
    @property
    def position(self) -> str:
        return self._position
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @property
    def leave_credits(self) -> int:
        return self._leave_credits
    
    @property
    def email(self) -> str:
        return self._email
    
    # Setters (Encapsulation - controlled access)
    @username.setter
    def username(self, value: str):
        self._username = value
    
    @password.setter
    def password(self, value: str):
        self._password = value
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @dept.setter
    def dept(self, value: str):
        self._dept = value
    
    @position.setter
    def position(self, value: str):
        self._position = value
    
    @phone.setter
    def phone(self, value: str):
        self._phone = value
    
    @leave_credits.setter
    def leave_credits(self, value: int):
        self._leave_credits = value
    
    @email.setter
    def email(self, value: str):
        self._email = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "username": self._username,
            "password": self._password,
            "role": self._role,
            "name": self._name,
            "dept": self._dept,
            "position": self._position,
            "phone": self._phone,
            "leave_credits": self._leave_credits,
            "email": self._email
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserModel':
        """Create user from dictionary"""
        return cls(
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=data.get("role", "user"),
            name=data.get("name", ""),
            dept=data.get("dept", ""),
            position=data.get("position", ""),
            phone=data.get("phone", ""),
            leave_credits=data.get("leave_credits", 15),
            email=data.get("email", "")
        )


class LeaveRequestModel:
    """Leave request model with encapsulated data"""
    
    def __init__(self, leave_id: int, username: str, leave_type: str,
                 start_date: str, end_date: str, reason: str,
                 status: str = "Pending", comment: str = "",
                 created_at: Optional[str] = None, seen: bool = False):
        self._leave_id = leave_id
        self._username = username
        self._leave_type = leave_type
        self._start_date = start_date
        self._end_date = end_date
        self._reason = reason
        self._status = status
        self._comment = comment
        self._created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self._seen = seen
    
    # Getters
    @property
    def leave_id(self) -> int:
        return self._leave_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def leave_type(self) -> str:
        return self._leave_type
    
    @property
    def start_date(self) -> str:
        return self._start_date
    
    @property
    def end_date(self) -> str:
        return self._end_date
    
    @property
    def reason(self) -> str:
        return self._reason
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def comment(self) -> str:
        return self._comment
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    @property
    def seen(self) -> bool:
        return self._seen
    
    # Setters
    @status.setter
    def status(self, value: str):
        self._status = value
    
    @comment.setter
    def comment(self, value: str):
        self._comment = value
    
    @seen.setter
    def seen(self, value: bool):
        self._seen = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self._leave_id,
            "username": self._username,
            "type": self._leave_type,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "reason": self._reason,
            "status": self._status,
            "comment": self._comment,
            "created_at": self._created_at,
            "seen": self._seen
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeaveRequestModel':
        """Create leave request from dictionary"""
        return cls(
            leave_id=data.get("id", 0),
            username=data.get("username", ""),
            leave_type=data.get("type", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            reason=data.get("reason", ""),
            status=data.get("status", "Pending"),
            comment=data.get("comment", ""),
            created_at=data.get("created_at"),
            seen=data.get("seen", False)
        )
    
    def get_date_range(self) -> str:
        """Get formatted date range"""
        return f"{self._start_date} to {self._end_date}"


class LeaveCreditHistoryModel:
    """Leave credit history model"""
    
    def __init__(self, username: str, action: str, amount: int, 
                 balance: int, reason: str, date: Optional[str] = None):
        self._username = username
        self._action = action
        self._amount = amount
        self._balance = balance
        self._reason = reason
        self._date = date or datetime.now().strftime("%Y-%m-%d %H:%M")
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def action(self) -> str:
        return self._action
    
    @property
    def amount(self) -> int:
        return self._amount
    
    @property
    def balance(self) -> int:
        return self._balance
    
    @property
    def reason(self) -> str:
        return self._reason
    
    @property
    def date(self) -> str:
        return self._date
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self._date,
            "action": self._action,
            "amount": self._amount,
            "balance": self._balance,
            "reason": self._reason
        }