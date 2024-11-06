from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name=_("email"))
    phone_number = PhoneNumberField(**NULLABLE, verbose_name=_("phone"))
    city = models.CharField(max_length=128, verbose_name=_("city"), **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars/", **NULLABLE, verbose_name=_("avatar")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return str(self.email)

class Payment(models.Model):
    METHOD_CHOICES = [
        (_("CASH"), _("cash")),
        (_("TRAN"), _("transfer to account")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name="payments", verbose_name=_("user"))
    date_payment = models.DateField(auto_now_add=True, verbose_name=_("date_payment"))
    paid_course = models.ForeignKey("materials.Course", on_delete=models.CASCADE, **NULLABLE, verbose_name=_("course"))
    paid_lesson = models.ForeignKey("materials.Lessons", on_delete=models.CASCADE, **NULLABLE, verbose_name=_("lessons"))
    amount = models.IntegerField(verbose_name=_("amount"))
    method = models.CharField(choices=METHOD_CHOICES, max_length=4, default="TRAN", verbose_name=_("method"))
    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
    def __str__(self):
        return f"{self.user} - {self.paid_course} - {self.paid_lesson}: {self.amount}"
