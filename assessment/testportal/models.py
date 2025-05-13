from django.db import models
from mentor.models import MentorProfile

# Create your models here.
class Question(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option_id = models.CharField(max_length=10)
    created_by = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)  # Teacher who made it
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question {self.id}: {self.question_text}"


class Test(models.Model):
    test_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    test_desc = models.TextField(max_length=500, blank=True)
    teacher = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)  # Teacher FK
    duration_minutes = models.PositiveIntegerField(default=0)  # Duration in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)  # Indicates if the test is currently active
    started = models.BooleanField(default=False)
    no_of_students = models.PositiveIntegerField(default=0)
    questions = models.ManyToManyField(Question, through='TestQuestion')

    def __str__(self):
        return f"Test {self.test_code}: {self.name}"


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"Test {self.test.test_code} - Question {self.question.id}"
