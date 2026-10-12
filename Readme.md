# 🏨 Hostel Management System

A web-based Hostel Management System built using **Python, FastAPI, Streamlit, SQLAlchemy, and MySQL**. The application provides separate portals for students and administrators to manage hostel activities through a user-friendly interface.

## 🚀 Features

### 👨‍🎓 Student Portal
- Secure student login with authentication.
- View student profile and personal details.
- View room allocation and accommodation details.
- Check hostel fee records and payment status.
- Submit and track complaints.
- View attendance records.
- View daily breakfast, lunch, and dinner menus.
- Apply for leave or outpass.
- Record food consumption.

### 🛡️ Admin Portal
- Secure administrator login.
- View hostel management dashboard.
- Manage student records.
- Manage hostel rooms.
- Allocate rooms to students.
- Manage fee records.
- View and manage complaints.
- Mark student attendance as Present or Absent.
- Manage daily food menus.
- View leave requests and food consumption records.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend REST API |
| Streamlit | Frontend web interface |
| MySQL | Relational database |
| SQLAlchemy | Database ORM |
| Uvicorn | FastAPI development server |
| Requests | Communication between frontend and backend |
| JWT | Token-based authentication, where configured |

## 📁 Project Structure

```text
hostel-management/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       └── routers/
│
├── frontend/
│   ├── app.py
│   └── hostel.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The exact backend file and router structure may differ depending on your implementation.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/hostel-management.git
cd hostel-management
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

1. Install and start MySQL.
2. Create the database:

```sql
CREATE DATABASE hostel_management;
```

3. Configure your database connection using environment variables or your project's existing configuration.
4. Ensure the required database tables are created using your application's setup or migration process.

**Security:** Do not commit database passwords, secret keys, access tokens, or real student information to GitHub.

### 5. Start the FastAPI backend

From the project root, if your application entry point is `backend/app/main.py`:

```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```

Open the API documentation at:

http://127.0.0.1:8000/docs

### 6. Start the Streamlit frontend

Open a second terminal from the project root:

```powershell
python -m streamlit run frontend/hostel.py
```

If your main frontend file is `app.py`, run:

```powershell
python -m streamlit run frontend/app.py
```

The frontend must use the correct FastAPI base URL. By default, local development uses:

```text
http://127.0.0.1:8000
```

## 🔐 Authentication

The application provides separate login options for students and administrators. Student registration may be available depending on the implemented backend routes. Administrator registration is not provided through the login page.

Authentication and authorization should be enforced by the backend for protected operations.

## 🧪 Testing

- Open FastAPI Swagger documentation to test API endpoints.
- Start the Streamlit application and test both portals.
- Verify that room, fee, attendance, complaint, leave, and food records are correctly stored in MySQL.
- Confirm that unauthorized users cannot access protected endpoints.

## 🔮 Future Enhancements

- Online fee payment integration.
- Email or SMS notifications.
- Advanced reports and analytics.
- Improved attendance reports.
- Deployment to a cloud platform.
- Automated testing and database migrations.

## 👨‍💻 Author

**Rohith Lokesh**

Artificial Intelligence and Machine Learning Engineering Student

## 📄 License

This project is intended for educational and academic purposes. Add a license file if you want to distribute it under specific terms.
