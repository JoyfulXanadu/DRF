from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from materials.models import Course, Lessons, Subscription
from users.models import User
class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_user = User.objects.create(
            email="test_user@gmail.com",
            first_name="test_user",
            last_name="test_user",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        moderators = Group.objects.create(name="moderator")
        self.test_moderator = User.objects.create(
            email="test_moderator@gmail.com",
            first_name="test_moderator",
            last_name="test_moderator",
            is_superuser=False,
            is_staff=True,
            is_active=True,
        )
        moderators.user_set.add(self.test_moderator)
        self.test_course = Course.objects.create(name="test_course", owner=self.test_user)
        self.test_lesson = Lessons.objects.create(name="test_lesson", course=self.test_course, owner=self.test_user)
        self.test_subscription = Subscription
        self.client.force_authenticate(user=self.test_user)
        # self.client.force_authenticate(user=self.test_moderator)
    def test_create_subscription(self):
        """
        Тестирование подписки и отписки на курс
        """
        url = reverse("materials:subscription_manage")
        data = {"course_id": self.test_course.pk,
                "name": "test_subscription"}
        # Подписка
        response = self.client.post(url, data)
        subscription = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(subscription['success'], 'subscription created')
        # Отписка
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)