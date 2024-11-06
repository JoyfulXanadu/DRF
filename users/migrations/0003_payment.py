# Generated by Django 5.1.2 on 2024-11-05 01:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_lessons_course_lessons_url"),
        ("users", "0002_remove_user_username_user_avatar_user_city_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_payment",
                    models.DateField(auto_now_add=True, verbose_name="date_payment"),
                ),
                ("amount", models.IntegerField(verbose_name="amount")),
                (
                    "method",
                    models.CharField(
                        choices=[("CASH", "cash"), ("TRAN", "transfer to account")],
                        default="TRAN",
                        max_length=4,
                        verbose_name="method",
                    ),
                ),
                (
                    "paid_course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materials.course",
                        verbose_name="course",
                    ),
                ),
                (
                    "paid_lesson",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materials.lessons",
                        verbose_name="lessons",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "payment",
                "verbose_name_plural": "payments",
            },
        ),
    ]
