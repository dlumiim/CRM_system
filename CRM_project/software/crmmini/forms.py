from django import forms
from .models import Project, CustomUser, Role, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'manager']
        labels = {
            'name': 'Название проекта',
            'manager': 'Руководитель проекта',
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date', 'role', 'stage']
        labels = {
            'title': 'Название задачи',
            'description': 'Описание задачи',
            'start_date': 'Дата начала выполнения',
            'end_date': 'Дата окончания выполнения',
            'role': 'Роль',
            'stage': 'Этап',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'middle_name', 'date_of_birth', 'phone_number', 'email', 'address', 'personal_id', 'role']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'date_of_birth': 'Дата рождения',
            'phone_number': 'Номер телефона',
            'email': 'Email',
            'address': 'Адрес',
            'personal_id': 'Личный ID',
            'role': 'Роль',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'registration_date': forms.DateInput(attrs={'type': 'date'}),
        }