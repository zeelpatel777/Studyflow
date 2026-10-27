from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from .models import Task, StudySession, UserProfile
import json


# ── Auth Views ──

def splash(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'studyflow/splash.html')


def login_view(request):
    error = None
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if not email or '@' not in email:
            error = 'Please enter a valid email address.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        else:
            # Try username = email or lookup by email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
            if user:
                login(request, user)
                return redirect('dashboard')
            error = 'Invalid email or password.'
    return render(request, 'studyflow/login.html', {'error': error})


def signup_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if not username:
            error = 'Username is required.'
        elif not email or '@' not in email:
            error = 'Enter a valid email.'
        elif len(password) < 6:
            error = 'Password must be 6+ characters.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        elif User.objects.filter(email=email).exists():
            error = 'Email already registered.'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'studyflow/signup.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('splash')


def reset_password(request):
    sent = False
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and '@' in email:
            sent = True   # In production: send real email via Django email backend
    return render(request, 'studyflow/reset_password.html', {'sent': sent})


# ── Main App Views ──

@login_required
def dashboard(request):
    today    = timezone.now().date()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    all_tasks  = request.user.tasks.filter(completed=False).order_by('deadline')
    upcoming   = request.user.tasks.filter(deadline__date__gt=today, completed=False)[:5]
    total      = request.user.tasks.count()
    done       = request.user.tasks.filter(completed=True).count()
    progress   = int((done / total * 100) if total else 0)
    focus_hrs  = profile.total_focus_hours()
    focus_pct  = min(int((focus_hrs / 8) * 100), 100)
    return render(request, 'studyflow/dashboard.html', {
        'all_tasks': all_tasks, 'upcoming': upcoming,
        'progress': progress, 'done': done, 'total': total,
        'profile': profile, 'focus_pct': focus_pct, 'focus_hrs': focus_hrs,
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        subject  = request.POST.get('subject', '').strip()
        desc     = request.POST.get('description', '').strip()
        deadline = request.POST.get('deadline')
        priority = request.POST.get('priority', 'medium')
        file     = request.FILES.get('file')
        if subject and deadline:
            Task.objects.create(
                user=request.user, subject=subject,
                description=desc, deadline=deadline,
                priority=priority, file=file,
            )
            messages.success(request, 'Task added!')
            return redirect('dashboard')
        messages.error(request, 'Subject and deadline are required.')
    return render(request, 'studyflow/task_create.html')


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = True
    task.save()
    return redirect('dashboard')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('dashboard')

@login_required
def focus_mode(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    timer_modes = [
        ('Focus Duration', 'work', '#1e3a8a', '#f8faff'),
        ('Short Break', 'short', '#22c55e', '#f0fdf4'),
        ('Long Break', 'long', '#f59e0b', '#fffbeb'),
    ]

    return render(request, 'studyflow/focus.html', {
        'profile': profile,
        'timer_modes': timer_modes,
    })

@login_required
def save_session(request):
    if request.method == 'POST':
        data    = json.loads(request.body)
        minutes = int(data.get('minutes', 0))
        if minutes > 0:
            StudySession.objects.create(user=request.user, duration_minutes=minutes)
    return JsonResponse({'status': 'ok'})


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.dark_mode     = 'dark_mode'     in request.POST
        profile.notifications = 'notifications' in request.POST
        profile.save()
        return redirect('profile')
    return render(request, 'studyflow/profile.html', {'profile': profile})
