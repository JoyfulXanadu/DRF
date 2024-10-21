from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YoutubeValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    #def create(self, validated_data):
        #lesson = validated_data.pop('lessons')
       # course = Course.objects.create(**validated_data)
       # for lesson in lesson:
           # Lesson.objects.create(course=course, **lesson)
           # return course

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    quantity_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_quantity_lesson(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'quantity_lesson', 'lessons')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
