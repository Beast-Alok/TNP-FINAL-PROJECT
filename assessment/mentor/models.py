from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    post = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    exp = models.CharField(max_length=10, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username