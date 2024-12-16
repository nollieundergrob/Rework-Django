# Django Application Documentation

This document provides an overview of the Django project, its structure, key features, and setup instructions.

---

## Project Overview

This Django project serves as a backend API with features like user authentication, group management, attendance tracking, scheduling, and library management for a local PyPI server. The application is built using the Django Rest Framework (DRF) and SimpleJWT for token-based authentication.

---

## Features

- **Authentication**: Token-based authentication using SimpleJWT.
- **User Management**: Create, update, and manage users with roles (student, teacher).
- **Group Management**: Define groups and assign users with specific roles.
- **Attendance Tracking**: Record attendance logs and associate files with attendance records.
- **Scheduling**: Manage group schedules and events.
- **Local PyPI Management**: Handle local Python package repositories, including package uploads, downloads, and metadata management.

---

## Project Structure

```plaintext
project-root/
├── application/           # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # App-specific URLs
│   ├── middleware.py      # Custom middlewares
│   ├── signals.py         # Django signals
│   ├── apps.py            # App configuration
│   ├── utils.py           # Utility functions
├── localpypi/             # Local PyPI Django app
│   ├── models.py          # Database models for local PyPI
│   ├── views.py           # API endpoints for package management
│   ├── serializers.py     # DRF serializers for PyPI libraries
│   ├── urls.py            # App-specific URLs for PyPI
│   ├── signals.py         # Django signals for library events
│   ├── apps.py            # App configuration for PyPI
├── config/                # Project-level configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Project-level URLs
│   ├── wsgi.py            # WSGI entry point
├── media/                 # Uploaded files
├── static/                # Static files (CSS, JS, etc.)
├── db.sqlite3             # SQLite database (default for development)
└── manage.py              # Django CLI utility
```

---

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the admin panel**:
   Navigate to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

---

## Key Modules

### `models.py`
Defines database models for users, groups, attendance records, schedules, and PyPI libraries.

### `views.py`
Provides class-based views for managing authentication, users, attendance records, groups, schedules, and PyPI libraries.

### `serializers.py`
Handles data serialization and deserialization for API endpoints, including PyPI library metadata.

### `middleware.py`
Custom middleware for JWT-based authentication.

### `signals.py`
Defines signal handlers for logging user login events and handling PyPI library updates.

---

## API Endpoints

### Authentication
- **Login**: `POST /auth/login/`
- **Refresh Token**: `POST /auth/refresh/`

### Users
- **List/Create Users**: `GET/POST /data/`
- **Update User**: `PUT/PATCH /data/<id>/`

### Attendance
- **List/Create Attendance**: `GET/POST /attendance/`
- **Download Aggregated Attendance**: `GET /attendance/aggregated/download/`

### Groups
- **List/Create Groups**: `GET/POST /groups/`
- **Add User to Group**: `POST /groups/<group_id>/add_user/`

### Schedules
- **List/Create Schedules**: `GET/POST /schedule/`

### Local PyPI
- **List Libraries**: `GET /simple/`
- **Library Details**: `GET /simple/<library_name>/`
- **Download Package File**: `GET /simple/<library_name>/<filename>/`

---

## Environment Variables

Ensure the following environment variables are set for production:

- `SECRET_KEY`: Secret key for Django.
- `DEBUG`: Set to `False` for production.
- `DATABASE_URL`: Database connection string.

---

## Testing

Run tests using the Django test framework:

```bash
python manage.py test
```

---

## Deployment

### Using Gunicorn and Nginx

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run Gunicorn**:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Set up Nginx**:
   Configure Nginx to proxy requests to the Gunicorn server.

### Using Docker (Optional)

1. **Build Docker Image**:
   ```bash
   docker build -t django-app .
   ```

2. **Run Docker Container**:
   ```bash
   docker run -d -p 8000:8000 django-app
   ```

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions or support, contact [your-email@example.com].
