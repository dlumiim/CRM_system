from django.core.management.base import BaseCommand
from crmmini.models import Project, CustomUser, Role, Task

class Command(BaseCommand):
    help = 'Initialize projects, users, and roles'

    def handle(self, *args, **kwargs):
        # Создание ролей (если ещё не созданы)
        role_it_manager, _ = Role.objects.get_or_create(name='Руководитель ИТ-проекта')
        role_executive, _ = Role.objects.get_or_create(name='Исполнители работ ИТ-проекта по функциональным направлениям (в том числе разработчики, тестировщики, технические писатели)')

        # Создание пользователей
        user1, _ = CustomUser.objects.get_or_create(username='user1', email='user1@example.com',
                                                   last_name='Иванов', first_name='Иван', middle_name='Иванович',
                                                   date_of_birth='1990-01-01', phone_number='+79001234567',
                                                   address='ул. Ленина, д. 1', personal_id='PID001', role='IT_PROJECT_MANAGER')
        user2, _ = CustomUser.objects.get_or_create(username='user2', email='user2@example.com',
                                                   last_name='Петров', first_name='Петр', middle_name='Петрович',
                                                   date_of_birth='1985-05-15', phone_number='+79007654321',
                                                   address='ул. Мира, д. 2', personal_id='PID002', role='EXECUTIVE')
        user3, _ = CustomUser.objects.get_or_create(username='user3', email='user3@example.com',
                                                   last_name='Сидоров', first_name='Сидор', middle_name='Сидорович',
                                                   date_of_birth='1992-11-20', phone_number='+79001122334',
                                                   address='ул. Советская, д. 3', personal_id='PID003', role='EXECUTIVE')

        # Создание проектов
        project1, _ = Project.objects.get_or_create(name='Проект 1', manager=user1)
        project2, _ = Project.objects.get_or_create(name='Проект 2', manager=user1)
        project3, _ = Project.objects.get_or_create(name='Проект 3', manager=user1)

        # Создание задач для проектов
        task1, _ = Task.objects.get_or_create(project=project1, title='Задача 1 проекта 1', description='Описание задачи 1 проекта 1',
                                              start_date='2023-10-01', end_date='2023-10-10', role=role_executive,
                                              stage='NEEDS_ASSESSMENT')
        task2, _ = Task.objects.get_or_create(project=project2, title='Задача 1 проекта 2', description='Описание задачи 1 проекта 2',
                                              start_date='2023-10-02', end_date='2023-10-15', role=role_executive,
                                              stage='ESTIMATION')
        task3, _ = Task.objects.get_or_create(project=project3, title='Задача 1 проекта 3', description='Описание задачи 1 проекта 3',
                                              start_date='2023-10-03', end_date='2023-10-20', role=role_executive,
                                              stage='PREPARATION')

        self.stdout.write(self.style.SUCCESS('Successfully initialized projects, users, and roles'))