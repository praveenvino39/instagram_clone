from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="auth/user/profile_picture", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    follow_request = models.JSONField(
        encoder=None, blank=True, null=True, default=[])
    following = models.JSONField(
        encoder=None, blank=True, null=True, default=[])
    followers = models.JSONField(
        encoder=None, blank=True, null=True, default=[])

    def __str__(self):
        return self.user.username
