from django.test import TestCase

from django.test import TestCase
from .models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = CustomUser.objects.create(
            username='testuser',
            role='IT_PROJECT_MANAGER',
            last_name='Иванов',
            first_name='Иван',
            email='ivanov@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'IT_PROJECT_MANAGER')
        self.assertEqual(str(self.user), 'Иванов Иван ()')

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'Иванов Иван ()')
