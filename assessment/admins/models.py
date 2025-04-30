from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class EmailInvitations(models.Model):
    email = models.EmailField(max_length=100, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.email