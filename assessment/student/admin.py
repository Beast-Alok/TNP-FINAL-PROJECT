from django.contrib import admin
from .models import StudentProfile, StudentSession, StudentAnswer
# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(StudentSession)
admin.site.register(StudentAnswer)