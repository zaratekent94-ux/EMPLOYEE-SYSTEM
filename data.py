# data.py
# =========================
# DATA MANAGER (Abstraction)
# =========================

from models import UserModel, LeaveRequestModel, LeaveCreditHistoryModel
from typing import List, Optional, Dict, Any


class DataManager:
    """
    DataManager class - encapsulates all data operations
    Uses ABSTRACTION to hide complex data management details
    """
    
    # Singleton instance
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Initialize data storage (Encapsulation - private attributes)
        self._users: List[UserModel] = []
        self._leave_requests: List[LeaveRequestModel] = []
        self._leave_credit_history: Dict[str, List[Dict[str, Any]]] = {}
        self._initialized = True
        
        # Initialize with default data
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize default users"""
        default_users = [
            UserModel("admin", "1", "admin", "Administrator", "IT", "System Admin", "+1234567890", 0),
            UserModel("john", "1", "user", "John Doe", "Engineering", "Software Engineer", "+1987654321", 30),
            UserModel("jane", "1", "user", "Jane Smith", "Human Resources", "HR Manager", "+1123456789", 30),
            UserModel("alice", "1", "user", "Alice Johnson", "Marketing", "Marketing Specialist", "+1098765432", 30),
            UserModel("bob", "1", "user", "Bob Brown", "Sales", "Sales Representative", "+1023456789", 30),
            UserModel("charlie", "1", "user", "Charlie Davis", "Finance", "Financial Analyst", "+1012345678", 30),
            UserModel("dave", "1", "user", "Dave Wilson", "Customer Support", "Support Specialist", "+1001234567", 30),  
            UserModel("eve", "1", "user", "Eve Miller", "Research and Development", "R&D Engineer", "+1234509876", 30)  
        ]
        self._users = default_users
    
    # =========================
    # USER OPERATIONS
    # =========================
    
    def get_all_users(self) -> List[UserModel]:
        """Get all users"""
        return self._users
    
    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username"""
        for user in self._users:
            if user.username == username:
                return user
        return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return role"""
        for user in self._users:
            if user.username == username and user.password == password:
                return user.role
        return None
    
    def add_user(self, user: UserModel) -> bool:
        """Add new user"""
        # Check if username already exists
        if self.get_user_by_username(user.username):
            return False
        
        self._users.append(user)
        return True
    
    def update_user(self, username: str, **kwargs) -> bool:
        """Update user attributes"""
        user = self.get_user_by_username(username)
        if not user:
            return False
        
        # Update only provided attributes
        if "name" in kwargs and kwargs["name"]:
            user.name = kwargs["name"]
        if "dept" in kwargs and kwargs["dept"]:
            user.dept = kwargs["dept"]
        if "position" in kwargs and kwargs["position"]:
            user.position = kwargs["position"]
        if "phone" in kwargs and kwargs["phone"]:
            user.phone = kwargs["phone"]
        if "password" in kwargs and kwargs["password"]:
            user.password = kwargs["password"]
        
        return True
    
    def delete_user(self, username: str) -> bool:
        """Delete user by username"""
        for i, user in enumerate(self._users):
            if user.username == username:
                self._users.pop(i)
                return True
        return False
    
    def get_users_by_role(self, role: str) -> List[UserModel]:
        """Get users by role"""
        return [user for user in self._users if user.role == role]
    
    # =========================
    # LEAVE REQUEST OPERATIONS
    # =========================
    
    def get_all_leave_requests(self) -> List[LeaveRequestModel]:
        """Get all leave requests"""
        return self._leave_requests
    
    def get_leave_requests_by_username(self, username: str) -> List[LeaveRequestModel]:
        """Get leave requests for a specific user"""
        return [leave for leave in self._leave_requests if leave.username == username]
    
    def add_leave_request(self, leave_request: LeaveRequestModel) -> bool:
        """Add new leave request"""
        self._leave_requests.append(leave_request)
        return True
    
    def update_leave_request(self, leave_id: int, **kwargs) -> bool:
        """Update leave request"""
        for leave in self._leave_requests:
            if leave.leave_id == leave_id:
                if "status" in kwargs:
                    leave.status = kwargs["status"]
                if "comment" in kwargs:
                    leave.comment = kwargs["comment"]
                if "seen" in kwargs:
                    leave.seen = kwargs["seen"]
                return True
        return False
    
    def get_leave_request_by_id(self, leave_id: int) -> Optional[LeaveRequestModel]:
        """Get leave request by ID"""
        for leave in self._leave_requests:
            if leave.leave_id == leave_id:
                return leave
        return None
    
    def get_next_leave_id(self) -> int:
        """Get next available leave ID"""
        if not self._leave_requests:
            return 1
        return max(leave.leave_id for leave in self._leave_requests) + 1
    
    # =========================
    # LEAVE CREDIT OPERATIONS
    # =========================
    
    def get_leave_credits(self, username: str) -> int:
        """Get leave credits for user"""
        user = self.get_user_by_username(username)
        return user.leave_credits if user else 0
    
    def update_leave_credits(self, username: str, credits: int) -> bool:
        """Update leave credits"""
        user = self.get_user_by_username(username)
        if user:
            user.leave_credits = credits
            return True
        return False
    
    def add_leave_credit_history(self, username: str, action: str, amount: int, 
                                  balance: int, reason: str):
        """Add leave credit history entry"""
        if username not in self._leave_credit_history:
            self._leave_credit_history[username] = []
        
        history = LeaveCreditHistoryModel(username, action, amount, balance, reason)
        self._leave_credit_history[username].append(history.to_dict())
    
    def get_leave_credit_history(self, username: str) -> List[Dict[str, Any]]:
        """Get leave credit history for user"""
        return self._leave_credit_history.get(username, [])
    
    # =========================
    # CONVERSION METHODS
    # =========================
    
    def users_to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert all users to dictionary list"""
        return [user.to_dict() for user in self._users]
    
    def leave_requests_to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert all leave requests to dictionary list"""
        return [leave.to_dict() for leave in self._leave_requests]


# Global data manager instance
data_manager = DataManager()