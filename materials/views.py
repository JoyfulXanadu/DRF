from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsModerator, IsOwner

from materials.models import Course, Lessons
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseDetailAPIView(CourseDetailSerializer):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return super().get_serializer_class()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (IsAuthenticated, ~IsModerator,)
        elif self.action == 'destroy':
            permission_classes = (IsAuthenticated, IsOwner)
        elif self.action in ['update', 'retrieve', 'partial_update']:
            permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        super().perform_create(new_course)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)


class LessonListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        super().perform_create(new_lesson)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)
