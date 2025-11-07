from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import DiaryEntry

User = get_user_model()


class SimpleDiaryTests(TestCase):
    """Простые тесты для быстрой проверки"""

    def setUp(self):
        # Создаем пользователя через стандартный метод
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('testpass123')
        self.user.save()

        # Создаем запись
        self.entry = DiaryEntry.objects.create(
            title='Простая запись',
            content='Простое содержание',
            author=self.user
        )

    def test_entry_created(self):
        """Простой тест создания записи"""
        self.assertEqual(DiaryEntry.objects.count(), 1)
        self.assertEqual(self.entry.title, 'Простая запись')
        self.assertEqual(self.entry.author, self.user)

    def test_privacy(self):
        """Простой тест приватности"""
        # Создаем второго пользователя
        user2 = User.objects.create(email='user2@example.com')
        user2.set_password('testpass123')
        user2.save()

        # Проверяем что пользователи видят только свои записи
        user1_entries = DiaryEntry.objects.filter(author=self.user)
        user2_entries = DiaryEntry.objects.filter(author=user2)

        self.assertEqual(user1_entries.count(), 1)
        self.assertEqual(user2_entries.count(), 0)