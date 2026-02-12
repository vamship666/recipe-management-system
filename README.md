# Recipe Management API

A production-ready RESTful API built using **Django** and **Django REST
Framework** that allows Creators to manage recipes and Viewers to
explore and favorite them.

---

## Features

### Authentication & Authorization

- Token-based authentication
- User registration & login
- Role-based access control:
  - **Creator** → Create, update, delete recipes
  - **Viewer** → View recipes and add to favorites

---

### Recipe Management

- Create recipes with:
  - Title
  - Description
  - Preparation & Cooking duration
  - Ingredients (nested)
  - Steps (ordered)
  - Optional thumbnail image
- Update & delete (Creator only)
- Optimized queries using `select_related` and `prefetch_related`

---

### Favorites System

- Viewers can add recipes to favorites
- Prevents duplicate favorites
- Unique constraint per user & recipe

---

### Bulk Upload

- Creators can upload recipes using:
  - CSV
  - Excel (.xlsx)

---

### PDF Export

Download recipe details as PDF:

GET /api/recipes/{id}/download_pdf/

---

### Pagination Example

{ "count": 4, "next": null, "previous": null, "results": \[\] }

---

### Filtering Examples

/api/recipes/?search=pasta\
/api/recipes/?ordering=-cook_duration

---

## Tech Stack

- Python 3.x
- Django 5.x
- Django REST Framework
- PostgreSQL
- drf-spectacular
- Token Authentication

---

## Setup Instructions

### Create Virtual Environment

python -m venv recipe_env
cd recipe_env\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Configure PostgreSQL

Create database: CREATE DATABASE recipe_db;

Update settings.py DATABASES accordingly.

### Run Migrations

python manage.py makemigrations
python manage.py migrate

### Create Superuser

python manage.py createsuperuser

### Run Server

python manage.py runserver

## 🔑 Important Endpoints

### Authentication

POST /api/accounts/register/\
POST /api/accounts/login/

### Recipes

GET /api/recipes/\
POST /api/recipes/\
POST /api/recipes/{id}/favourite/\
GET /api/recipes/{id}/download_pdf/

### Favorites

GET /api/favorites/

## API Documentation

Swagger UI: http://127.0.0.1:8000/api/docs/

## 👨‍💻 Project Highlights

✔ Authentication & Authorization\
✔ Role-Based Access\
✔ Nested Serializers\
✔ Pagination & Filtering\
✔ Bulk Upload\
✔ PDF Generation\
✔ Production-ready structure
