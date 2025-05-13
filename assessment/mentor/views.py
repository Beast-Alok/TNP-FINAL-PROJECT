from django.shortcuts import render
from admins.models import EmailInvitations
from .models import MentorProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import random
import string
from datetime import datetime
import json
from django.http import JsonResponse
from testportal.models import Test, Question, TestQuestion
from django.urls import reverse
from announcements_manager.models import Announcements
from django.utils import timezone
# Create your views here.

@login_required(login_url='/auth/login/')
def mentorhome(request):
    if hasattr(request.user, 'mentorprofile'):
        if request.method == 'POST':
            test_name = request.POST.get('test')
            test_desc = request.POST.get('test_desc')
            test_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            created_at = datetime.now()
            print(test_code, test_name, test_desc, created_at)
            test = Test.objects.create(
                test_code=test_code,
                name=test_name,
                test_desc=test_desc,
                created_at=created_at,
                teacher=request.user.mentorprofile
            )
            test.save()
            print(test_code, test_name, test_desc, created_at)
            return redirect(f"{reverse('make_test_next')}?test_code={test_code}")
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'mentor_home.html')


@login_required(login_url='/auth/login/')
def make_test_next(request):
    if hasattr(request.user, 'mentorprofile'):
        test_code = request.GET.get('test_code')  # <-- get test_code from URL
        return render(request, 'make_question_phase.html', {'test_code': test_code})
    else:
        messages.error(request, "Only mentors can access this page.")
        return render(request, 'make_question_phase.html')

@login_required(login_url='/auth/login/')
def save_questions(request):
    data = json.loads(request.body)
    duration = data.get('duration')
    test_code = data.get('test_code')
    try:
        test = Test.objects.get(test_code=test_code)
        test.duration_minutes = duration
        for q in data['questions']:
            id = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            q = Question.objects.create(
                id = id,
                question_text=q['question'],
                option_a=q['options'][0],
                option_b=q['options'][1],
                option_c=q['options'][2],
                option_d=q['options'][3],
                correct_option_id=q['correct'],
                created_by=test.teacher,
                created_at=datetime.now()
            )
            q.save()

            tq = TestQuestion.objects.create(
                test=test,
                question=q,
            )
            tq.save()
        test.save()

    except Test.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)
    
    return JsonResponse({'status': 'ok'})

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
    if hasattr(request.user, 'mentorprofile'):
        profile = request.user.mentorprofile
        tests = Test.objects.filter(teacher=profile)
        return render(request, 'view_test_reports.html', {'tests': tests})
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'view_test_reports.html')


@login_required(login_url='/auth/login/')
def mentor_announcements(request):
    if hasattr(request.user, 'mentorprofile'):
        if request.method == 'POST':
            message = request.POST.get('announcement_text')
            announ = Announcements.objects.create(
                author=request.user.mentorprofile,
                message=message,
                created_at=timezone.now()
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'ok',
                    'message': announ.message,
                    'author': str(announ.author),
                    'created_at': announ.created_at.strftime('%Y-%m-%d %H:%M')
                })
            announ.save()
            print(announ.created_at)
        
        announs = Announcements.objects.all().order_by('-created_at')
        return render(request, 'mentor_announcements.html', {'announs' : announs})
        
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
                user = User.objects.create_user(username=username, password=password)
                user.save()
                mentor_profile = MentorProfile.objects.create(
                    user=user,
                    email=email, 
                    name=name,
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