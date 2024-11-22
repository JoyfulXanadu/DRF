from django.core.mail import send_mail
from celery import shared_task
from config import settings
from materials.models import Subscription, Course


@shared_task
def send_update_course_course(course_pk: int) -> None:
    course = Course.objects.select_related('owner').get(pk=course_pk)
    subs = Subscription.objects.filter(course=course)
    emails = subs.values_list('user__email', flat=True)
    if not emails:
        return

    send_mail(
        subject="Update course",
        message=f"The owner {course.owner.email} updated his course {course.name}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
    )
