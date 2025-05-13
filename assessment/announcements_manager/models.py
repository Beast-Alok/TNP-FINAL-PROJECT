from django.db import models
from mentor.models import MentorProfile
# Create your models here.

class Announcements(models.Model):
    author = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Announcements {self.author}"