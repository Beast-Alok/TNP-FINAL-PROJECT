# Generated by Django 5.2 on 2025-05-07 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testportal', '0003_test_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testquestion',
            name='order',
        ),
    ]
