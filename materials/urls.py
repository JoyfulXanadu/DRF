from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView,
                             SubscriptionCreateDestroyAPIView
                             )

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet, basename='course')

urlpatterns = [

    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/create", LessonCreateAPIView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path(
        "lessons/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lessons_delete"
    ),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),

    path("subscription_manage/", SubscriptionCreateDestroyAPIView.as_view(), name="subscription_manage"),
    # path("subscription_list/", SubscriptionListAPIView.as_view(), name="subscription_list"),
] + router.urls
