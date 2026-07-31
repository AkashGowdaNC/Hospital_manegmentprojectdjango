# Hospital Management Django Project

A Django-based hospital management system for managing patients, doctors, appointments, and hospital information.

## Project Structure

- `hospital_management/hospital_management/hospital_management/`: Django project root containing `manage.py` and project settings.
- `hospital_management/hospital_management/hospital_management/core/`: Django app with models, views, forms, templates, and URLs.
- `hospital_management/hospital_management/hospital_management/hospital/`: Django project configuration.
- `hospital_management/hospital_management/hospital_management/templates/`: shared templates and UI pages.
- `hospital_management/hospital_management/hospital_management/static/`: static assets.
- `hospital_management/hospital_management/hospital_management/db.sqlite3`: SQLite database file.

## Features

- User authentication and login
- Doctor management
- Patient management
- Appointment scheduling and listing
- Dashboard and detail views
- Data stored using SQLite
- Static file handling with WhiteNoise

## Requirements

- Python 3.10+ (recommended)
- Django 4.2.7
- Pillow
- django-widget-tweaks
- whitenoise

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/AkashGowdaNC/Hospital_manegmentprojectdjango.git
cd Hospital_manegmentprojectdjango
```

2. Navigate to the Django project folder:

```bash
cd hospital_management/hospital_management/hospital_management
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python manage.py migrate
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Open the site in your browser:

```
http://127.0.0.1:8000/
```

## Notes

- The project uses SQLite and the database file is stored at `hospital_management/hospital_management/hospital_management/db.sqlite3`.
- Static files are collected in `staticfiles/` and configured with WhiteNoise.
- The Django settings currently use `DEBUG = True` and allow all hosts.
- `SECRET_KEY` is set for local development and should be updated before production use.

## Hospital Information

The current hospital configuration is defined in `hospital/settings.py`:

- Name: `Clover Hospital`
- Address: `Hassan, Karnataka`
- Phone: `+91-8123-456789`
- Email: `info@cloverhospital.com`
- Emergency Contact: `+91-9876-543210`

## Optional Commands

- Create a superuser:

```bash
python manage.py createsuperuser
```

- Collect static files:

```bash
python manage.py collectstatic
```

- Run tests:

```bash
python manage.py test
```

## Cleanup

The repository contains `venv` and `venv_new` directories in the project folder. These are ignored by `.gitignore` and should not be committed.
