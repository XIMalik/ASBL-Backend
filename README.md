# School Admissions & Content Platform

A Django-based backend system for managing school admissions, programs, faculty, and content with role-based access control.

## Database Schema

### Core Models
- **profiles**: System users (admin, reviewer, user)
- **programs**: Academic programs with details and enrollment
- **people**: Faculty, mentors, and staff
- **program_people**: Junction table for program-person relationships
- **news**: School announcements and articles

### Admissions Models
- **applications**: Student applications to programs
- **admin_requests**: Requests for admin privileges

## Features

- UUID primary keys for all models
- Role-based permissions (public, user, reviewer, admin)
- PostgreSQL with proper indexing
- RESTful API with Django REST Framework
- Auto-updating timestamps
- Strong foreign key relationships

## Setup Instructions

### 1. Database Setup
```bash
# Create PostgreSQL database
createdb school_db

# Or using psql
psql -U postgres
CREATE DATABASE school_db;
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Sample Data
```bash
python manage.py create_sample_data
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

## API Endpoints

### Core Endpoints
- `GET/POST /api/programs/` - List/create programs
- `GET/POST /api/people/` - List/create people
- `GET/POST /api/news/` - List/create news
- `GET /api/news/featured/` - Get featured news
- `GET /api/programs/{id}/people/` - Get people for a program

### Admissions Endpoints
- `GET/POST /api/applications/` - List/create applications
- `PATCH /api/applications/{id}/update_status/` - Update application status
- `GET/POST /api/admin-requests/` - List/create admin requests
- `PATCH /api/admin-requests/{id}/review/` - Review admin requests

## Permissions

### Public (Unauthenticated)
- Read: programs, news, people
- Create: applications

### Authenticated Users (role=user)
- Read: own applications, own profile
- Create: admin requests

### Reviewers (role=reviewer)
- Read: all applications
- Update: application status

### Admins (role=admin)
- Full CRUD on all models
- Approve/reject admin requests
- Manage programs and people

## Database Indexes

The following indexes are automatically created:
- `profiles.email`
- `applications.program_id`
- `applications.email`
- `applications.status`
- `admin_requests.email`
- `admin_requests.status`

## Sample Data

Run `python manage.py create_sample_data` to populate the database with:
- Sample profiles (admin, reviewer, user)
- Academic programs (Computer Science, Business)
- Faculty members
- News articles
- Sample applications and admin requests