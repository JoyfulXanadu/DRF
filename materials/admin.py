from django.contrib import admin

from materials.models import Course, Lessons
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name", "description")
@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "url",
        "course",
    )
    search_fields = ("name", "description")
    list_filter = ("course",)