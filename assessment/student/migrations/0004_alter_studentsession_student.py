# Generated by Django 5.2 on 2025-05-05 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_studentanswer_question_studentsession_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsession',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile'),
        ),
    ]
