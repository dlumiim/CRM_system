from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, CustomUser, Role, Task
from .forms import ProjectForm, TaskForm, UserForm
from django.forms import modelformset_factory
from django.db.models import Q
from django.contrib import messages


def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})


def projects_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'name')  # По умолчанию сортируем по названию проекта

    projects = Project.objects.all()

    if query:
        projects = projects.filter(Q(name__icontains=query))

    if sort_by == 'date':
        projects = projects.order_by('-created_at')
    elif sort_by == 'status':
        projects = projects.order_by('status')

    return render(request, 'projects_list.html', {'projects': projects})


def add_project(request):
    TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1, can_delete=False)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, prefix='project')
        task_formset = TaskFormSet(request.POST, prefix='task')

        if project_form.is_valid() and task_formset.is_valid():
            project = project_form.save(commit=False)
            project.save()

            for task_form in task_formset:
                task = task_form.save(commit=False)
                if task_form.cleaned_data:
                    task.project = project
                    task.save()

            return redirect('projects_list')
    else:
        project_form = ProjectForm(prefix='project')
        task_formset = TaskFormSet(prefix='task', queryset=Task.objects.none())  # Инициализируем с пустым queryset
        roles = Role.objects.all()  # Получаем все роли из базы данных
        users = CustomUser.objects.all()  # Получаем всех пользователей из базы данных

    return render(request, 'add_project.html', {
        'project_form': project_form,
        'task_formset': task_formset,
        'roles': roles,
        'users': users,
    })


def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1, can_delete=False)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, prefix='project', instance=project)
        task_formset = TaskFormSet(request.POST, prefix='task', queryset=project.tasks.all())

        if project_form.is_valid() and task_formset.is_valid():
            project = project_form.save(commit=False)
            project.save()

            for task_form in task_formset:
                task = task_form.save(commit=False)
                if task_form.cleaned_data:
                    task.project = project
                    task.save()

            return redirect('projects_list')
    else:
        project_form = ProjectForm(prefix='project', instance=project)
        task_formset = TaskFormSet(prefix='task', queryset=project.tasks.all())
        roles = Role.objects.all()  # Получаем все роли из базы данных
        users = CustomUser.objects.all()  # Получаем всех пользователей из базы данных

    return render(request, 'edit_project.html', {
        'project_form': project_form,
        'task_formset': task_formset,
        'roles': roles,
        'users': users,
    })


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован!')
            return redirect('register_user')
        else:
            messages.error(request, 'Ошибка при регистрации пользователя.')
    else:
        form = UserForm()
        roles = Role.objects.all()

    return render(request, 'register_user.html', {'form': form, 'roles': roles})