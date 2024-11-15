from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsSelf
from users.serializers import (
    PaymentSerializer,
    UserDetailSerializer,
    UserSerializer,
    UserShortSerializer,
)
from users.services import convert_rub_to_usd, create_stripe_price, create_stripe_session


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return UserShortSerializer
        elif self.action == "retrieve":
            return UserDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "create":
            permission_classes = (AllowAny,)
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = (IsAuthenticated, IsSelf)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_user = serializer.save(is_active=True)
        new_user.set_password(new_user.password)
        super().perform_create(new_user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if obj == self.request.user:
            self.check_object_permissions(self.request, obj)
            return obj
        raise PermissionDenied


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_course", "paid_lessons", "method")
    ordering_fields = ("date_payment",)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollar = convert_rub_to_usd(payment.amount)
        price = create_stripe_price(amount_in_dollar)
        session_id, url = create_stripe_session(price)
        payment.session_id = session_id
        payment.url = url
        super().perform_create(payment)
