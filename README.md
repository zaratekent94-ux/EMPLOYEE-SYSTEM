# Presented by:
## BSCS 1A
## Kent S. Zarate, Charlene I. Vano, Christian Maki M. Bayonas, Antonio Gabriel V. Lupian


# Title
## The Employee Information And Leave Management System

# Description
An employee and leave management system is designed to serve as a centralized platform for managing employee related data and leave process within an organization. Its purpose is to securely store and organize employee information while efficiently handling leave records, requests, approvals, and balances. By integrating employee information with leave management, the system ensures accuracy, consistency, and accessibility of data, supporting smooth human resource operations and effective workforce management.

# Prerequisites:
Before installing the Employee Information and Leave Management System, make sure you have the following tools and software installed:
-Python 3.x – to run the backend
-Flask – web framework for building the system
-SQLite (or other database) – to store employee data and leave records
-HTML & CSS – for designing the user interface
-Code editor (like VS Code or PyCharm) – to view and edit the project files
-Web browser – to access and test the system

# Installation:

1.install flask - pip instal flask

2.Clone the project files

3.Navigate to the project folder:
cd project-folder

4.Install required Python packages:
pip install -r requirements.txt

5.Run the application:
python app.py

6.Open the system in your browser:
Go to http://127.0.0.1:5000/

Usage:
After running the Employee Information and Leave Management System, you can use it as follows:

1.Open your browser and go to:
http://127.0.0.1:5000/

2.Log in with your username and password choose wha role you have (admin/employee).
3.Access the system features:
  -Admin Dashboard
  -Employee Dashboard

4.Example (Python code to run the app):
from app import app
app.run(debug=True)

# Module 1
Login Module/ Login System: This is the first completed and functioning module of our Employee Information and Leave Management System. It allows users to securely log in using their username and password base on there role(Admin/Employee), ensuring that only authorized personnel can access the system. The module includes input validation to prevent incorrect or unauthorized entries and provides error messages for invalid login attempts. The login page is designed to be user-friendly and responsive, making it easy for users to navigate. By completing this module, we have established a secure and functional foundation for the rest of the system, which will handle employee records, leave requests, and other important features.

Functionalites:
- Create User Account (Admin, Employee)
The system allows the creation of different types of user accounts, such as admin and employee. Each account has specific roles and permissions within the system.

- Login and Logout System
Users can securely log in to access the system and log out after use. This helps protect accounts and ensures that only authorized users can access the system.

# Module 2
Stage 2 focuses on the **Employee Account** module, which manages the storage and maintenance of employee information. In this stage, the system allows the storage of personal and job-related details while ensuring data accuracy through controlled updates of employee records. Access is strictly regulated: only HR or Admin personnel are permitted to edit or modify records, while employees are limited to viewing their own profiles. This ensures data security and prevents unauthorized changes. The flowchart below illustrates the step-by-step process, including account creation, verification, updating of records, and viewing of employee information, ensuring an organized and secure management system for all employee data.

Functionalites:
- Store Personal and Job Details
The system keeps important employee information such as name, position, department, and contact details. This serves as the main record for each employee.

- Update Employee Records
The system allows updates to employee information when needed, such as changes in position or contact details, to keep records accurate and up to date.

# Module 3
This module allows authorized personnel such as supervisors or HR administrators to review employee leave requests and make decisions based on company policies. The admin can either approve or deny requests while providing comments to justify their decision. The system ensures that all approvals follow established company rules and guidelines. Additionally, it tracks the status of each request, allowing both administrators and employees to monitor progress and outcomes efficiently.

Functionalities:
- Review and Approve/Deny Requests
Admins or supervisors can check each leave request submitted by employees and decide whether to approve or deny it based on valid reasons and available leave balance.

- Add Comments
The approver can include comments or explanations when approving or rejecting a request. This helps employees understand the decision clearly.

- Track Approval Status
The system keeps track of the current status of each request, such as pending, approved, or denied. This allows both admins and employees to monitor progress.

# Module 4
This module manages and monitors employees leave credits within the system. It automatically updates leave balances whenever a leave request is approved, ensuring that deductions are accurately recorded. The system enforces rules to prevent employees from exceeding their available leave credits. Additionally, it displays the remaining leave balance for transparency and tracking purposes. If applicable, leave credits are reset annually based on company policy, ensuring proper allocation for each new period.

Functionalities:
- Automatically Update Leave Credits
The system automatically adjusts an employee’s leave balance whenever a leave request is approved. This means the number of available leave days is always updated without manual computation.

- Show Remaining Leaves
Employees can view how many leave credits they still have. This helps them plan their leaves properly and avoid exceeding their allowed number of days.

# Module 5
This stage focuses on organizing, generating, and exporting important data from the system. It allows authorized users, such as admins or HR staff, to access summarized information about employees and their leave records.

Functionalities:
- Generate Employee and Leave Reports
The system can automatically create reports that show important details such as employee information, leave history, and leave balances. These reports help in monitoring employee attendance, tracking leave usage, and supporting decision-making.

- Export Files (PDF/Excel)
Users can download or export these reports into file formats like PDF or Excel. This makes it easier to print, share, or store records for documentation and future reference.

# Module 6 
This stage focuses on keeping users informed about important actions and updates in the system. It ensures that employees and administrators receive timely alerts regarding leave requests and approvals.

Functionalities:
- Send Alerts for Approval and Updates
The system automatically sends notifications when there are updates, such as when a leave request is approved, rejected, or still pending. This helps users stay informed without needing to manually check the system.

- Email/SMS Notifications
Notifications can be delivered through email or SMS, allowing users to receive updates even when they are not logged into the system. This improves communication and responsiveness.

# Vercel.app
https://employee-system-7gti.vercel.app/user_dashboard

# admin username and password
username = admin
password = 1

# employee username and password
username = eve
password = 1