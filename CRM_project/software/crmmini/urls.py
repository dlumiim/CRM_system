from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('users/register/', views.register_user, name='register_user'),
]