# Dashboard app is stats-only for now; it composes data from other apps.
# Add an Announcement model here if you want the Notice Board (module 12) backed by real data.
from django.db import models
from django.conf import settings


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_pinned = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title
