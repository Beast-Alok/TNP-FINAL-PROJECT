# Generated by Django 5.2 on 2025-04-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_userprofile_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
