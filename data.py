# data.py
# =========================
# DATA MANAGER (Abstraction)
# =========================

from models import UserModel, LeaveRequestModel, LeaveCreditHistoryModel
from typing import List, Optional, Dict, Any
from datetime import datetime


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
            UserModel("admin", "1", "admin", "Administrator", "IT", "System Admin", "+1234567890", 0, "admin@company.com"),
            UserModel("john", "1", "user", "John Doe", "Engineering", "Software Engineer", "+1987654321", 30, "john.doe@company.com"),
            UserModel("jane", "1", "user", "Jane Smith", "Human Resources", "HR Manager", "+1123456789", 30, "jane.smith@company.com"),
            UserModel("alice", "1", "user", "Alice Johnson", "Marketing", "Marketing Specialist", "+1098765432", 30, "alice.johnson@company.com"),
            UserModel("bob", "1", "user", "Bob Brown", "Sales", "Sales Representative", "+1023456789", 30, "bob.brown@company.com"),
            UserModel("charlie", "1", "user", "Charlie Davis", "Finance", "Financial Analyst", "+1012345678", 30, "charlie.davis@company.com"),
            UserModel("dave", "1", "user", "Dave Wilson", "Customer Support", "Support Specialist", "+1001234567", 30, "dave.wilson@company.com"),  
            UserModel("eve", "1", "user", "Eve Miller", "Research and Development", "R&D Engineer", "+1234509876", 30, "eve.miller@company.com")  
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
        if "email" in kwargs and kwargs["email"]:
            user.email = kwargs["email"]
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
    
    # =========================
    # REPORT DATA METHODS
    # =========================
    
    def get_employee_report_data(self) -> List[Dict[str, Any]]:
        """Get employee report data - all users with details"""
        report_data = []
        for user in self._users:
            # Get leave statistics for this user
            user_leaves = self.get_leave_requests_by_username(user.username)
            pending = sum(1 for l in user_leaves if l.status == "Pending")
            approved = sum(1 for l in user_leaves if l.status == "Approved")
            rejected = sum(1 for l in user_leaves if l.status == "Rejected")
            
            report_data.append({
                "username": user.username,
                "name": user.name,
                "dept": user.dept,
                "position": user.position,
                "phone": user.phone,
                "leave_credits": user.leave_credits,
                "role": user.role,
                "leave_requests": len(user_leaves),
                "pending_leaves": pending,
                "approved_leaves": approved,
                "rejected_leaves": rejected
            })
        return report_data
    
    def get_leave_report_data(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get leave report data with optional filters"""
        leaves = self._leave_requests
        
        # Apply filters if provided
        if filters:
            if "status" in filters and filters["status"]:
                leaves = [l for l in leaves if l.status == filters["status"]]
            if "username" in filters and filters["username"]:
                leaves = [l for l in leaves if l.username == filters["username"]]
            if "leave_type" in filters and filters["leave_type"]:
                leaves = [l for l in leaves if l.leave_type == filters["leave_type"]]
            if "start_date" in filters and filters["start_date"]:
                leaves = [l for l in leaves if l.start_date >= filters["start_date"]]
            if "end_date" in filters and filters["end_date"]:
                leaves = [l for l in leaves if l.end_date <= filters["end_date"]]
        
        report_data = []
        for leave in leaves:
            user = self.get_user_by_username(leave.username)
            report_data.append({
                "leave_id": leave.leave_id,
                "username": leave.username,
                "employee_name": user.name if user else "Unknown",
                "dept": user.dept if user else "",
                "leave_type": leave.leave_type,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "reason": leave.reason,
                "status": leave.status,
                "comment": leave.comment,
                "created_at": leave.created_at
            })
        return report_data
    
    def get_report_statistics(self) -> Dict[str, Any]:
        """Get overall report statistics"""
        total_employees = len(self._users)
        total_leaves = len(self._leave_requests)
        
        status_counts = {"Pending": 0, "Approved": 0, "Rejected": 0}
        leave_type_counts = {}
        
        for leave in self._leave_requests:
            status_counts[leave.status] = status_counts.get(leave.status, 0) + 1
            leave_type_counts[leave.leave_type] = leave_type_counts.get(leave.leave_type, 0) + 1
        
        # Department distribution
        dept_counts = {}
        for user in self._users:
            dept_counts[user.dept] = dept_counts.get(user.dept, 0) + 1
        
        return {
            "total_employees": total_employees,
            "total_leave_requests": total_leaves,
            "status_breakdown": status_counts,
            "leave_type_breakdown": leave_type_counts,
            "department_breakdown": dept_counts,
            "active_users": len([u for u in self._users if u.role == "user"])
        }


# Global data manager instance
data_manager = DataManager()


# =========================
# NOTIFICATION SERVICE
# =========================

class NotificationService:
    """
    NotificationService - handles real-time notifications
    Supports in-app notifications (expandable for email/SMS)
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Notification storage: {username: [notifications]}
        self._notifications: Dict[str, List[Dict[str, Any]]] = {}
        self._initialized = True
    
    def add_notification(self, username: str, notification_type: str, title: str, 
                        message: str, priority: str = "normal") -> bool:
        """Add a notification for a user"""
        if username not in self._notifications:
            self._notifications[username] = []
        
        notification = {
            "id": len(self._notifications[username]) + 1,
            "type": notification_type,
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "read": False
        }
        
        self._notifications[username].append(notification)
        return True
    
    def get_notifications(self, username: str, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get notifications for a user"""
        notifications = self._notifications.get(username, [])
        
        if unread_only:
            return [n for n in notifications if not n.get("read", False)]
        
        return notifications
    
    def mark_as_read(self, username: str, notification_id: int) -> bool:
        """Mark a notification as read"""
        notifications = self._notifications.get(username, [])
        
        for notif in notifications:
            if notif["id"] == notification_id:
                notif["read"] = True
                return True
        
        return False
    
    def mark_all_as_read(self, username: str) -> int:
        """Mark all notifications as read for a user"""
        notifications = self._notifications.get(username, [])
        count = 0
        
        for notif in notifications:
            if not notif.get("read", False):
                notif["read"] = True
                count += 1
        
        return count
    
    def get_unread_count(self, username: str) -> int:
        """Get count of unread notifications"""
        notifications = self._notifications.get(username, [])
        return sum(1 for n in notifications if not n.get("read", False))
    
    def clear_notifications(self, username: str) -> bool:
        """Clear all notifications for a user"""
        if username in self._notifications:
            self._notifications[username] = []
            return True
        return False
    
    # =========================
    # EMAIL/SMS NOTIFICATION METHODS
    # =========================
    
    def send_email_notification(self, email: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Send email notification (placeholder - integrate with SMTP/email service)
        Returns status of the send operation
        """
        # Anti-spam checks
        if len(subject) > 200:
            return {"success": False, "error": "Subject too long (max 200 characters)"}
        
        if len(body) > 5000:
            return {"success": False, "error": "Body too long (max 5000 characters)"}
        
        # Check for spam patterns
        spam_keywords = ["free", "win", "prize", "urgent", "click here", "buy now"]
        body_lower = body.lower()
        if any(keyword in body_lower for keyword in spam_keywords):
            return {"success": False, "error": "Message flagged as potential spam"}
        
        # Check for excessive URLs
        url_count = body_lower.count("http")
        if url_count > 3:
            return {"success": False, "error": "Too many URLs (max 3)"}
        
        # Placeholder for email integration
        # In production, integrate with SMTP, SendGrid, etc.
        return {
            "success": True,
            "method": "email",
            "recipient": email,
            "subject": subject,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def send_sms_notification(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Send SMS notification (placeholder - integrate with SMS gateway)
        Returns status of the send operation
        """
        # Anti-spam checks
        if len(message) > 160:  # Standard SMS length
            return {"success": False, "error": "Message too long (max 160 characters)"}
        
        # Check for spam patterns
        spam_keywords = ["free", "win", "prize", "urgent", "call now", "text back"]
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in spam_keywords):
            return {"success": False, "error": "Message flagged as potential spam"}
        
        # Check for excessive URLs or phone numbers
        url_count = message_lower.count("http")
        if url_count > 1:
            return {"success": False, "error": "Too many URLs in SMS"}
        
        phone_count = len([word for word in message.split() if word.replace("-", "").replace("(", "").replace(")", "").isdigit() and len(word) > 7])
        if phone_count > 1:
            return {"success": False, "error": "Too many phone numbers in SMS"}
        
        # Placeholder for SMS integration
        # In production, integrate with Twilio, Nexmo, etc.
        return {
            "success": True,
            "method": "sms",
            "recipient": phone,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def notify_leave_status_change(self, username: str, leave_id: int, 
                                   status: str, comment: str = "") -> bool:
        """Send notification when leave status changes"""
        user = data_manager.get_user_by_username(username)
        if not user:
            return False
        
        title = f"Leave Request {status}"
        message = f"Your leave request (ID: {leave_id}) has been {status}."
        if comment:
            message += f" Comment: {comment}"
        
        # Add in-app notification
        self.add_notification(username, "leave_status", title, message, "high" if status == "Rejected" else "normal")
        
        return True
    
    def notify_new_leave_request(self, admin_username: str, username: str, 
                                 leave_id: int, leave_type: str) -> bool:
        """Notify admin of new leave request"""
        title = "New Leave Request"
        message = f"{username} submitted a new {leave_type} leave request (ID: {leave_id})"
        
        self.add_notification(admin_username, "new_leave", title, message, "high")
        return True


# Global notification service instance
notification_service = NotificationService()