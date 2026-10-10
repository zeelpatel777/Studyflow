from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from .models import Task, StudySession, UserProfile
import json


def splash(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'studyflow/splash.html')


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        error = 'Invalid credentials. Please try again.'
    return render(request, 'studyflow/login.html', {'error': error})


def signup_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'studyflow/signup.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('splash')


@login_required
def dashboard(request):
    today = timezone.now().date()
    tasks_today = request.user.tasks.filter(deadline__date=today, completed=False)
    upcoming = request.user.tasks.filter(deadline__date__gt=today, completed=False)[:3]
    total = request.user.tasks.count()
    done = request.user.tasks.filter(completed=True).count()
    progress = int((done / total * 100) if total else 0)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'studyflow/dashboard.html', {
        'tasks_today': tasks_today,
        'upcoming': upcoming,
        'progress': progress,
        'done': done,
        'total': total,
        'profile': profile,
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            subject=request.POST.get('subject'),
            description=request.POST.get('description', ''),
            deadline=request.POST.get('deadline'),
            priority=request.POST.get('priority', 'medium'),
        )
        return redirect('dashboard')
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
    return render(request, 'studyflow/focus.html', {'profile': profile})


@login_required
def save_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        minutes = data.get('minutes', 0)
        if minutes > 0:
            StudySession.objects.create(user=request.user, duration_minutes=minutes)
    return JsonResponse({'status': 'ok'})


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.dark_mode = 'dark_mode' in request.POST
        profile.notifications = 'notifications' in request.POST
        profile.save()
        return redirect('profile')
    return render(request, 'studyflow/profile.html', {'profile': profile})
