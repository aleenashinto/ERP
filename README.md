# Office ERP System

A full-stack Office ERP built with **Django + Django REST Framework** (backend) and
**React** (frontend). JWT authentication, role-based access control, and six working
modules: Authentication, User Management, Departments, Employee Directory, Attendance,
and Leave Management, plus a live Dashboard tying them together.

This has been tested end-to-end (migrations run cleanly, API endpoints verified with
curl, React build compiles with no errors) so it's a solid base to build the rest of
your ERP spec on top of.

## Tech stack

- **Backend:** Python, Django 5, Django REST Framework, Simple JWT, django-cors-headers, django-filter
- **Frontend:** React 18, React Router, Axios, Recharts
- **Database:** SQLite by default (zero config) — switch to PostgreSQL by editing `.env`
- **Auth:** JWT (access + refresh tokens, auto-refresh on the frontend)

## What's implemented

| Module | Backend | Frontend |
|---|---|---|
| Authentication (login, logout, JWT, forgot/reset/change password) | ✅ | ✅ Login page |
| User Management & RBAC (Super Admin, HR, Manager, Team Lead, Employee, Accountant) | ✅ | ✅ role-aware UI |
| Department Management (CRUD, head, employee count) | ✅ | ✅ |
| Employee Directory (search, filter by dept/status/designation) | ✅ | ✅ |
| Attendance (check-in/out, late flag, monthly view) | ✅ | ✅ |
| Leave Management (apply/cancel/approve/reject, balances, reports) | ✅ | ✅ |
| Dashboard (stat cards, charts, birthdays, department distribution) | ✅ | ✅ |
| Notice Board (Announcement model + API) | ✅ | — (add a page reusing the pattern below) |

## Extending to the rest of your spec

The remaining modules from your feature list (Payroll, Projects, Tasks, Inventory,
Expenses, Clients, Invoices, Meetings, Calendar, Messaging, Recruitment, Performance,
Reports, Audit Logs, Settings, AI features) follow the **exact same pattern** used here:

1. `python manage.py startapp <name>` inside `backend/`, add it to `INSTALLED_APPS`
2. `models.py` → `serializers.py` → `views.py` (ModelViewSet) → `urls.py` (DefaultRouter)
3. Wire the app's urls into `office_erp/urls.py`
4. On the frontend, add a page under `src/pages/<Name>/`, call it via `src/services/api.js`,
   and add it to the sidebar in `src/components/Layout.js` and the routes in `src/App.js`

The `accounts.permissions` module (`IsHR`, `IsManagerOrAbove`, `IsAccountant`, etc.) is
reusable for locking down any new endpoint by role.

## Getting started

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # edit if you want Postgres instead of SQLite

python manage.py migrate
python manage.py seed_demo_data   # creates demo admin/HR/employee accounts
python manage.py runserver
```

Backend runs at `http://127.0.0.1:8000`. Demo logins created by `seed_demo_data`:

| Username | Password | Role |
|---|---|---|
| `admin` | `Admin@12345` | Super Admin |
| `hr_jane` | `Hr@12345` | HR |
| `john_dev` | `John@12345` | Employee |

Django admin is available at `/admin/` with the `admin` account.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local    # points at the backend API, edit if needed
npm start
```

Frontend runs at `http://localhost:3000` and proxies API calls to the URL in
`REACT_APP_API_URL`.

### 3. Log in

Open `http://localhost:3000`, sign in with any demo account above, and explore the
Dashboard, Employees, Departments, Attendance, and Leaves pages. Try logging in as
`john_dev` (Employee) vs `hr_jane` (HR) to see the role-based UI differences —
e.g. only HR/Admin can add departments, and only managers can approve/reject leave.

## Project structure

```
office_erp/
├── backend/
│   ├── office_erp/        # settings, root urls
│   ├── accounts/          # custom User model, roles, JWT auth, permissions
│   ├── employees/         # employee profiles & directory
│   ├── departments/       # department CRUD
│   ├── attendance/        # check-in/out, monthly reports
│   ├── leaves/             # leave requests, balances, approvals
│   ├── dashboard/         # aggregate stats + announcements
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/          # Login, Dashboard, Employees, Departments, Attendance, Leaves
    │   ├── components/     # Layout (sidebar), IdBadge, Pill
    │   ├── context/        # AuthContext (JWT login/logout state)
    │   ├── services/       # axios instance with auto token refresh
    │   └── routes/         # PrivateRoute guard
    └── package.json
```


