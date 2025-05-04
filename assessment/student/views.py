from django.shortcuts import render
from .models import StudentProfile  # Import your profile model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# if request.user.is_authenticated:
#     try:
#         profile = StudentProfile.objects.get(user=request.user)
#     except StudentProfile.DoesNotExist:
#         profile = None

@login_required(login_url='/auth/login/')
def home(request):
    profile = None
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'home.html', {'profile': profile})

@login_required(login_url='/auth/login/')
def test(request):
    profile = None
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'test.html')

@login_required(login_url='/auth/login/')
def view_mentor(request):
    profile = None
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'mentor.html')

@login_required(login_url='/auth/login/')
def history(request):
    profile = None
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'history.html')

@login_required(login_url='/auth/login/')
def announcement(request):
    profile = None
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'announcements.html')

@login_required(login_url='/auth/login/')
def community(request):
    profile = None
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'community.html')

