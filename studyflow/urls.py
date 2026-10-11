from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.splash,          name='splash'),
    path('login/',              views.login_view,      name='login'),
    path('signup/',             views.signup_view,     name='signup'),
    path('logout/',             views.logout_view,     name='logout'),
    path('reset-password/',     views.reset_password,  name='reset_password'),
    path('dashboard/',          views.dashboard,       name='dashboard'),
    path('task/new/',           views.task_create,     name='task_create'),
    path('task/<int:pk>/done/', views.task_complete,   name='task_complete'),
    path('task/<int:pk>/del/',  views.task_delete,     name='task_delete'),
    path('focus/',              views.focus_mode,      name='focus'),
    path('focus/save/',         views.save_session,    name='save_session'),
    path('profile/',            views.profile_view,    name='profile'),
]
