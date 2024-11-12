from django.db import models
from django.utils.translation import gettext_lazy as _
from config import settings

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    preview = models.ImageField(
        upload_to="courses", verbose_name=_("preview"), **NULLABLE
    )
    description = models.TextField(verbose_name=_("description"), **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name=_("onwer"))

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")


class Lessons(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"), **NULLABLE)
    preview = models.ImageField(
        upload_to="lessons", verbose_name=_("preview"), **NULLABLE
    )
    url = models.TextField(**NULLABLE, verbose_name=_("url"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name=_("course"),related_name="lessons")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name=_("owner"))

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")

class Subscription(models.Model):

    name = models.CharField(max_length=128, verbose_name=_("name"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name=_("user"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name=_("course"))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    def __str__(self):
        return str(self.course)
    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
