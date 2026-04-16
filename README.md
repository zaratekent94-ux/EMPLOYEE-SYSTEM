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

# Module 2
Stage 2 focuses on the **Employee Account** module, which manages the storage and maintenance of employee information. In this stage, the system allows the storage of personal and job-related details while ensuring data accuracy through controlled updates of employee records. Access is strictly regulated: only HR or Admin personnel are permitted to edit or modify records, while employees are limited to viewing their own profiles. This ensures data security and prevents unauthorized changes. The flowchart below illustrates the step-by-step process, including account creation, verification, updating of records, and viewing of employee information, ensuring an organized and secure management system for all employee data.
