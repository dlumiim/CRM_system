from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('IT_PROJECT_MANAGER', 'Руководитель ИТ-проекта'),
        ('SUBCONTRACTOR_PROJECT_MANAGER', 'Руководитель ИТ-проекта от подрядчика'),
        ('LEAD_ARCHITECT', 'Главный архитектор ИТ-проекта'),
        ('SECURITY_ARCHITECT', 'Архитектор по ИБ'),
        ('INTEGRATION_ARCHITECT', 'Архитектор по межсистемной интеграции'),
        ('INFRASTRUCTURE_ARCHITECT', 'Архитектор по инфраструктуре'),
        ('BUSINESS_ANALYST', 'Бизнес-аналитик'),
        ('IT_PROJECT_ADMIN', 'Администратор ИТ-проекта'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='IT_PROJECT_MANAGER')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    middle_name = models.CharField(max_length=150, verbose_name='Отчество', blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    address = models.TextField(verbose_name='Адрес', blank=True, null=True)
    personal_id = models.CharField(max_length=50, verbose_name='Личный ID', unique=True, blank=True, null=True)
    registration_date = models.DateField(default=timezone.now, verbose_name='Дата регистрации')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        role_display = dict(self.ROLE_CHOICES).get(self.role, '')
        full_name = f"{self.last_name} {self.first_name} {self.middle_name or ''} ({role_display})"
        return full_name.strip().replace('  ', ' ')


class Project(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('IN_PROGRESS', 'В процессе'),
        ('COMPLETED', 'Завершен'),
    ]
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_projects', limit_choices_to={'role': 'IT_PROJECT_MANAGER'})
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='NEW')
    members = models.ManyToManyField(CustomUser, related_name='projects', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.auto_assign_members()

    def auto_assign_members(self):
        developers = CustomUser.objects.filter(role='EXECUTIVE')
        self.members.set(developers)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class DocumentTemplate(models.Model):
    name = models.CharField(max_length=200)
    template_file = models.FileField(upload_to='templates/')

    def __str__(self):
        return self.name


class UploadedDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name} - {self.document.name}"


class Task(models.Model):
    STAGE_CHOICES = [
        ('NEEDS_ASSESSMENT', 'Выявление потребностей'),
        ('ESTIMATION', 'Оценка'),
        ('PREPARATION', 'Подготовка'),
        ('DESIGN', 'Проектирование'),
        ('SOLUTION_CREATION', 'Создание решения'),
        ('LAUNCH_PREPARATION', 'Подготовка к запуску'),
        ('LAUNCH', 'Запуск'),
        ('SUPPORT', 'Поддержка'),
        ('MONITORING', 'Мониторинг'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='NEEDS_ASSESSMENT')

    def save(self, *args, **kwargs):
        if not self.assigned_to:
            # Назначаем ответственного человека автоматически
            available_users = CustomUser.objects.filter(role=self.role).exclude(projects=self.project)
            if available_users.exists():
                self.assigned_to = available_users.first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.title}"