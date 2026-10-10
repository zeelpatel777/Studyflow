# StudyFlow — Django Web App

Student study planner with 6 screens matching the UI/UX design.

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create superuser (optional, for /admin)
python manage.py createsuperuser

# 4. Start server
python manage.py runserver
```

Then open: http://127.0.0.1:8000

## Screens

| URL | Screen |
|-----|--------|
| `/` | Splash screen |
| `/login/` | Login |
| `/signup/` | Sign up |
| `/dashboard/` | Home dashboard |
| `/task/new/` | Task creation |
| `/focus/` | Focus mode (Pomodoro) |
| `/profile/` | Profile + stats |
| `/admin/` | Django admin panel |

## Features
- User auth (signup / login / logout)
- Create tasks with subject, deadline, priority (High / Medium / Low)
- Mark tasks complete, delete tasks
- Progress bar on dashboard
- Pomodoro timer with 25/5/15 modes
- Rotating motivational quotes
- Study session auto-saved after Pomodoro
- Profile with stats (tasks done, focus hours, streak)
- Dark mode toggle (persists per user)
