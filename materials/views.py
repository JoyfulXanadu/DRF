from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials import serializers
from materials.models import Course, Lessons, Subscription
from materials.paginators import CustomPagination
from materials.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by("pk")
    serializer_class = serializers.CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CourseDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "create":
            permission_classes = (
                IsAuthenticated,
                ~IsModerator,
            )
        elif self.action == "destroy":
            permission_classes = (IsAuthenticated, IsOwner)
        elif self.action in ["update", "retrieve", "partial_update"]:
            permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        super().perform_create(new_course)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderator").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lessons.objects.all().order_by("pk")
    serializer_class = serializers.LessonSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        super().perform_create(new_lesson)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class SubscriptionCreateDestroyAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message, stat = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(message, status=stat, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        message = {}

        course = generics.get_object_or_404(Course.objects.all(), pk=course_id)

        old_subscription = Subscription.objects.filter(user=user, course=course)
        if old_subscription.exists():

            old_subscription.delete()
            message["success"] = _("subscription removed")
            stat = status.HTTP_204_NO_CONTENT
        else:

            new_subscription = serializer.save(user=user, course=course)
            super().perform_create(new_subscription)
            message["success"] = _("subscription created")
            stat = status.HTTP_201_CREATED
        return message, stat


# class SubscriptionListAPIView(generics.ListAPIView):
#     queryset = Subscription.objects.all()
#     serializer_class = serializers.SubscriptionSerializer
