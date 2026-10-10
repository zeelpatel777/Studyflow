from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.subject


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    duration_minutes = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.duration_minutes}min on {self.date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    streak = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)

    def total_focus_hours(self):
        total = sum(s.duration_minutes for s in self.user.sessions.all())
        return round(total / 60, 1)

    def completed_tasks(self):
        return self.user.tasks.filter(completed=True).count()

    def __str__(self):
        return f"{self.user.username}'s profile"
