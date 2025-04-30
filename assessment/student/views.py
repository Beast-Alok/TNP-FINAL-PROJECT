from django.shortcuts import render
from .models import StudentProfile  # Import your profile model
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/auth/login/')
def home(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            profile = None
    return render(request, 'home.html', {'profile': profile})

@login_required(login_url='/auth/login/')
def test(request):
    return render(request, 'test.html')

@login_required(login_url='/auth/login/')
def view_mentor(request):
    return render(request, 'mentor.html')

@login_required(login_url='/auth/login/')
def history(request):
    return render(request, 'history.html')

@login_required(login_url='/auth/login/')
def announcement(request):
    return render(request, 'announcements.html')

@login_required(login_url='/auth/login/')
def community(request):
    return render(request, 'community.html')

