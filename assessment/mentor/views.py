from django.shortcuts import render
from admins.models import EmailInvitations
from .models import MentorProfile
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'mentor_home.html')

def info(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        college = request.POST.get('college')
        mobile = request.POST.get('mobile')
        post = request.POST.get('post')
        subject = request.POST.get('subject')
        experience = request.POST.get('experience')
        # Process the form data here

        try:
            email_invitation = EmailInvitations.objects.get(verification_code=code)
            if email_invitation.email == email:
                # Create a new user and mentor profile
                user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
                user.save()
                mentor_profile = MentorProfile.objects.create(
                    user=user,
                    college=college,
                    mobile=mobile,
                    subject=subject,
                    exp=experience,
                    post=post,
                    is_approved=True
                )
                mentor_profile.save()
                # Optionally, delete the email invitation after use
                email_invitation.delete()
                messages.success(request, 'Mentor profile created successfully!')
            else:
                messages.error(request, 'Email does not match the verification code.')
        except EmailInvitations.DoesNotExist:
            messages.error(request, 'Invalid verification code.')
    return render(request, 'info.html')