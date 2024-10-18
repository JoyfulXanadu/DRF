from django.contrib import admin
from django.urls import path

from lms.models import Course, Lesson

admin.site.register(Course)
admin.site.register(Lesson)


def site():
    return None