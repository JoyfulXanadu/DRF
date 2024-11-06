from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    preview = models.ImageField(
        upload_to="courses", verbose_name=_("preview"), **NULLABLE
    )
    description = models.TextField(verbose_name=_("description"), **NULLABLE)

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

    class Meta:
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")
