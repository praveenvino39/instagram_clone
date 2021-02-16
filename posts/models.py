from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, related_name="user",
                             related_query_name="user", on_delete=models.CASCADE)
    video_url = models.URLField(blank=False, null=True)
    caption = models.TextField(blank=True, null=True)
    is_video = models.BooleanField(default=False)
    post_image = models.ImageField(blank=True, null=True)
    likes = models.JSONField(encoder=None, blank=True, null=True, default=[])
    comments = models.JSONField(
        encoder=None, blank=True, null=True, default=[])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.caption)
