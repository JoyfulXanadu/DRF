from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="materials/", **NULLABLE, verbose_name="Изображение"
    )
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    preview = models.ImageField(upload_to="materials/", **NULLABLE, verbose_name="Изображение")
    video_link = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="Курс")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
