***Blood Bank System***
**Overview**
*The Blood Bank System is a web application designed to facilitate blood donation and blood requests. It connects donors with individuals or organizations in need of blood, streamlining the process of donation and request management.*

**Features**
User authentication (Signup/Login)
Role-based user management (Donor/Hospital)
Blood donation registration
Blood request submission
Viewing available blood donors
Profile management for donors
Administrative dashboard for managing users and requests

**Technologies Used**
Backend: Django
Frontend: HTML, CSS
Database: SQLite 
Deployment: PythonAnywhere 

**Installation**
Prerequisites
Make sure you have the following installed:

Python 3.x
pip (Python package installer)
Git
Clone the Repository
bash
Copy code
git clone https://github.com/aking-283/blood-bank-System-.git
cd blood-bank-System-
Set Up Virtual Environment
bash
Copy code
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
Install Requirements
bash
Copy code
pip install -r requirements.txt
Migrate Database
bash
Copy code
python manage.py migrate
Create a Superuser
bash
Copy code
python manage.py createsuperuser
Run the Development Server
bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/.

Deployment
This project is deployed on PythonAnywhere . You can access the live version at:

https://puspak1.pythonanywhere.com/

Usage
Navigate to the homepage.
As a donor, you can register your details and availability.
As a user in need, you can request blood from registered donors.

**Contributing**
Contributions are welcome! Please fork the repository and submit a pull request for any features or fixes.
