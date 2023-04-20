import os
import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.reverse import reverse_lazy

from CarShowRoom.settings import USER_CONFIRMATION_KEY, USER_CONFIRMATION_TIMEOUT


def send_verification_email(instance, topic: str, message_before_link: str, request):
    """Function that creates and sends verification link to instances email"""

    token = uuid.uuid4().hex
    redis_key = USER_CONFIRMATION_KEY.format(token=token)
    cache.set(redis_key, {"user_id": instance.pk}, timeout=USER_CONFIRMATION_TIMEOUT)
    confirm_link = request.build_absolute_uri(
        reverse_lazy("tokens:email_confirm", kwargs={"token": token})
    )
    send_mail(
        topic,
        f"{message_before_link}\n{confirm_link}",
        os.getenv("EMAIL_USER"),
        [instance.email],
    )
