import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.reverse import reverse_lazy

from CarShowRoom.settings import USER_CONFIRMATION_KEY, USER_CONFIRMATION_TIMEOUT


class EmailVerificationMixin:
    """Mixin with sending email function for serializers and views"""

    def send_verification_email(
        self, instance, topic: str, message_before_link: str, request=None
    ):
        token = uuid.uuid4().hex
        redis_key = USER_CONFIRMATION_KEY.format(token=token)
        cache.set(
            redis_key, {"user_id": instance.pk}, timeout=USER_CONFIRMATION_TIMEOUT
        )
        if request is None:
            request = self.context["request"]
        confirm_link = request.build_absolute_uri(
            reverse_lazy("tokens:email_confirm", kwargs={"token": token})
        )
        send_mail(
            topic,
            f"{message_before_link}\n{confirm_link}",
            "akeonst@yandex.ru",
            [instance.email],
        )
