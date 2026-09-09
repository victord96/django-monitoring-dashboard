from django.db import models
from django.conf import settings
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel


class Report(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    file = models.FileField(null=False, blank=False)
    file_content_type = models.CharField(max_length=127, null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(null=False, blank=False, default=timezone.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["-date", "-modified"]

    def __str__(self):
        return self.name
