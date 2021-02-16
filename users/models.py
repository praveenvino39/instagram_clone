from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=1000, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    following = models.JSONField(
        encoder=None, blank=True, null=True, default=[])
    followers = models.JSONField(
        encoder=None, blank=True, null=True, default=[])

    def __str__(self):
        return self.user.username
