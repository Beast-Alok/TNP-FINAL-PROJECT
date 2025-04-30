from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    enrollment_number = models.CharField(max_length=20, blank=True)
    year_of_study = models.CharField(max_length=10, blank=True)
    college_id = models.ImageField(upload_to='college_ids/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username