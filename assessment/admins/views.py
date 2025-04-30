from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from student.models import StudentProfile
from admins.models import EmailInvitations
from django.core.mail import send_mail
import random

def home(request):
    # Fetch all verified users
    verified_users = StudentProfile.objects.filter(is_verified=True, is_approved=False)
    return render(request, 'admins.html', {'verified_users': verified_users})

def approve_user(request, user_id):
    if request.method == 'POST':
        user_profile = get_object_or_404(StudentProfile, id=user_id)
        user_profile.is_approved = True
        user_profile.save()
        messages.success(request, f"{user_profile.user.first_name} has been approved.")
    return redirect('admin_home')  # Replace 'admin_home' with the name of your admin home URL

def reject_user(request, user_id):
    if request.method == 'POST':
        user_profile = get_object_or_404(StudentProfile, id=user_id)
        user_profile.user.delete()  # Delete the associated user
        user_profile.delete()  # Delete the user profile
        messages.error(request, f"{user_profile.user.first_name} has been rejected and removed.")
    return redirect('admin_home')  # Replace 'admin_home' with the name of your admin home URL

def mentor_invite(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # print(email)
        if EmailInvitations.objects.filter(email=email).exists():
            messages.error(request, f"An invitation has already been sent to {email}")
            return redirect('mentor_invite')  # Replace 'mentor_invite' with the name of your invite URL
        obj = EmailInvitations.objects.create(
            email=email,
            verification_code=str(random.randint(100000, 999999))
        )
        obj.save()

        subject = 'Email Verification'
        message = (
            f"Dear Mentor,\n\n"
            f"We are excited to invite you to join our platform as a mentor to teach and guide students. "
            f"Your expertise and knowledge can make a significant impact on their learning journey.\n\n"
            f"To get started, please use the following verification code to register on our platform:\n\n"
            f"Verification Code: {obj.verification_code}\n\n"
            f"Visit the following link to complete your registration:\n"
            f"http://127.0.0.1:8000/mentor/info/\n\n"
            f"Thank you for your willingness to contribute to the growth of our students.\n\n"
            f"Best regards,\n"
            f"The Team"
        )
        from_email = 'noreply@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, f"Invitation sent to {email}")
    return render(request, 'invite.html')