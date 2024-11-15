from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class URLCorrectValidator:
    def __init__(self, field: str, url: str):
        self.field = field
        self.url = url

    def __call__(self, value):
        url = value.get(self.field)
        if url:
            if not url.lower().startswith(self.url):
                message = _(
                    f"The link {url} is incorrect. The link should start with {self.url}"
                )
                raise serializers.ValidationError(message)
