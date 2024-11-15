from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lessons
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
        self.test_course = Course.objects.create(
            name="test_course", owner=self.test_user
        )
        self.test_lesson = Lessons.objects.create(
            name="test_lesson", course=self.test_course, owner=self.test_user
        )
        self.client.force_authenticate(user=self.test_user)

    def test_lessons_list(self):
        """
        Тестирование получения списка уроков
        """
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        lessons = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(lessons.get("results")[0].get("name"), self.test_lesson.name)

    def test_lessons_create(self):
        """
        Тестирование создания урока
        """
        url = reverse("materials:lessons_create")
        data = {"name": "test_create"}
        response = self.client.post(url, data=data)
        lesson = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(lesson.get("name"), data["name"])

    def test_lessons_update(self):
        url = reverse("materials:lessons_update", args=(self.test_lesson.pk,))
        data = {"name": "test_update"}
        response = self.client.patch(url, data=data)
        lesson = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.get("name"), data["name"])

    def test_lessons_retrieve(self):
        """
        Тестирование получения урока
        """
        url = reverse("materials:lessons_retrieve", args=(self.test_lesson.pk,))
        response = self.client.get(url)
        lesson = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.get("name"), self.test_lesson.name)

    def test_lessons_destroy(self):
        """
        Тестирование удаления урока
        """
        url = reverse("materials:lessons_delete", args=(self.test_lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Course

    def test_course_list(self):
        """
        Тестирование получения списка уроков
        """
        url = reverse("materials:course-list")
        response = self.client.get(url)
        courses = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            courses,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.test_course.pk,
                        "name": self.test_course.name,
                        "preview": None,
                        "description": None,
                        "owner": self.test_course.owner.pk,
                    }
                ],
            },
        )

    def test_course_create(self):
        """
        Тестирование создания курса
        """
        url = reverse("materials:course-list")
        data = {"name": "test_create"}
        response = self.client.post(url, data=data)
        courses = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(courses.get("name"), data["name"])

    def test_course_update(self):
        """
        Тестирование редактирования курса
        """
        url = reverse("materials:course-detail", args=(self.test_course.pk,))
        data = {"name": "test_update"}
        response = self.client.patch(url, data=data)
        course = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(course.get("name"), data["name"])

    def test_course_retrieve(self):
        """
        Тестирование получения курса
        """
        url = reverse("materials:course-detail", args=(self.test_course.pk,))
        response = self.client.get(url)
        course = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(course.get("name"), self.test_course.name)

    def test_course_destroy(self):
        """
        Тестирование удаления курса
        """
        url = reverse("materials:course-detail", args=(self.test_course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
