from django.contrib import admin
from .models import Question, Test, TestQuestion
# Register your models here.

admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestQuestion)