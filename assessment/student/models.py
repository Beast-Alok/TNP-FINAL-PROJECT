from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.utils.timezone import now
from testportal.models import Test, Question

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
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
    community = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class StudentSession(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    question_order = models.JSONField(default=list)  # Stores list of question IDs in order
    current_index = models.PositiveIntegerField(default=0)  # Tracks progress

    def __str__(self):
        return f"{self.student.user.username} - {self.test.name}"

class StudentAnswer(models.Model):
    session = models.ForeignKey(StudentSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session.student.user.username} - {self.question.id} - {self.selected_option}"
