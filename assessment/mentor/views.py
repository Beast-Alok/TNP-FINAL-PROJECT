from django.shortcuts import render
from admins.models import EmailInvitations
from .models import MentorProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.

@login_required(login_url='/auth/login/')
def mentorhome(request):
    if hasattr(request.user, 'mentorprofile'):
        profile = request.user.mentorprofile
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'mentor_home.html')


@login_required(login_url='/auth/login/')
def take_test(request):
    profile = None
    if hasattr(request.user, 'mentorprofile'):
        profile = request.user.mentorprofile
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'take_test.html')


@login_required(login_url='/auth/login/')
def view_test(request):
    profile = None
    if hasattr(request.user, 'mentorprofile'):
        profile = request.user.mentorprofile
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'view_test_reports.html')


@login_required(login_url='/auth/login/')
def mentor_announcements(request):
    profile = None
    if hasattr(request.user, 'mentorprofile'):
        profile = request.user.mentorprofile
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'mentor_announcements.html')


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
                return redirect('login')
            else:
                messages.error(request, 'Email does not match the verification code.')
        except EmailInvitations.DoesNotExist:
            messages.error(request, 'Invalid verification code.')
    return render(request, 'info.html')