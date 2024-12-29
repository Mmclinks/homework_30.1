from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course, Subscription, Lesson

class LessonTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя, администратора, курс и урок
        self.user = get_user_model().objects.create_user(
            email='user@example.com', password='password123')
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com', password='password123')
        self.course = Course.objects.create(
            name='Test Course',
            description='Description of the test course'
        )
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Description of the test lesson',
            video_url='http://example.com/video',
            course=self.course
        )

    def test_create_lesson_as_admin(self):
        """Тестируем создание урока для администратора."""
        url = reverse('courses:lesson-list', kwargs={'course_id': self.course.id})
        data = {
            'name': 'New Lesson',
            'description': 'New lesson description',
            'video_url': 'http://example.com/new_video',
            'course': self.course.id
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # Урок должен быть создан


    def test_create_lesson_as_user(self):
        """Тестируем создание урока для обычного пользователя (доступ запрещен)."""
        url = reverse('courses:lesson-list', kwargs={'course_id': self.course.id})
        data = {
            'name': 'New Lesson',
            'description': 'New lesson description',
            'video_url': 'http://example.com/new_video',
            'course': self.course.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)


    def test_update_lesson_as_admin(self):
        """Тестируем обновление урока для администратора."""
        url = reverse('courses:lesson-update', kwargs={'course_id': self.course.id, 'pk': self.lesson.id})
        data = {
            'name': 'Updated Lesson',
            'description': 'Updated description',
            'video_url': 'http://example.com/updated_video',
            'course': self.course.id
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_update_lesson_as_user(self):
        """Тестируем обновление урока для обычного пользователя (доступ запрещен)."""
        url = reverse('courses:lesson-update', kwargs={'course_id': self.course.id, 'pk': self.lesson.id})
        data = {
            'name': 'Updated Lesson',
            'description': 'Updated description',
            'video_url': 'http://example.com/updated_video',
            'course': self.course.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_as_admin(self):
        """Тестируем удаление урока для администратора."""
        url = reverse('courses:lesson-delete', kwargs={'course_id': self.course.id, 'pk': self.lesson.id})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_as_user(self):
        """Тестируем удаление урока для обычного пользователя (доступ запрещен)."""
        url = reverse('courses:lesson-delete', kwargs={'course_id': self.course.id, 'pk': self.lesson.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = get_user_model().objects.create_user(
            email='user@example.com', password='password123')

        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com', password='password123')

        # Создаем курс
        self.course = Course.objects.create(
            name='Test Course',
            description='Description of the test course'
        )

    def test_subscribe_to_course(self):
        """Тестируем подписку на курс."""
        url = reverse('courses:subscribe')  # Здесь предполагается URL для подписки
        data = {
            'course_id': self.course.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription = Subscription.objects.get(user=self.user, course=self.course)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)

    def test_unsubscribe_from_course(self):
        """Тестируем отписку от курса."""
        Subscription.objects.create(user=self.user, course=self.course)  # Создаем подписку
        url = reverse('courses:subscribe')  # Здесь предполагается URL для отписки
        data = {
            'course_id': self.course.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Subscription.DoesNotExist):
            Subscription.objects.get(user=self.user, course=self.course)  # Проверяем, что подписка удалена
