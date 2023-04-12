from django.db import models
from django.utils import timezone


class DefaultFields(models.Model):
    created_at = models.DateTimeField(default=timezone.now())
    modified_at = models.DateTimeField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
