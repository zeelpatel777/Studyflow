# StudyFlow — Django Web App

## Setup & Run

```bash
# 1. Install
pip install -r requirements.txt

# 2. Migrate
python manage.py makemigrations studyflow
python manage.py migrate

# 3. Run
python manage.py runserver
```

Open: http://127.0.0.1:8000

## Pages
| URL | Page |
|-----|------|
| `/` | Splash |
| `/login/` | Login |
| `/signup/` | Sign Up |
| `/reset-password/` | Reset Password |
| `/dashboard/` | Dashboard |
| `/task/new/` | Create Task |
| `/focus/` | Focus Mode (Pomodoro) |
| `/profile/` | Profile & Settings |
| `/admin/` | Admin Panel |
