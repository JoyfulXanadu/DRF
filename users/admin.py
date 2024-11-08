from django.contrib import admin

from users.models import User, Payment
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "phone_number",
        "city",
    )
    search_fields = ("email", "phone_number")
    list_filter = ("city",)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date_payment",
        "paid_course",
        "paid_lesson",
        "amount",
        "method",
    )
    search_fields = ("user",)
    ordering = ("date_payment",)
    list_filter = ("paid_course", "paid_lesson", "method")
