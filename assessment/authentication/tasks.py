from celery import shared_task
from student.models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def schedule_account_deletion(user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = StudentProfile.objects.get(user=user)

        # Check if the user is still unverified
        if not profile.is_verified:
            profile.delete()  # Delete the StudentProfile
            user.delete()  # Delete the associated User
            return f"Deleted unverified account for user ID {user_id}."
        return f"User ID {user_id} is already verified."
    except User.DoesNotExist:
        return f"User ID {user_id} does not exist."
    except StudentProfile.DoesNotExist:
        return f"StudentProfile for user ID {user_id} does not exist."