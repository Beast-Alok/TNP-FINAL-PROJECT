from django.shortcuts import redirect
from django.urls import path, include

def home(request):
    redirect_url = 'student/'  # URL to redirect to
    return redirect(redirect_url)  # Redirect to the specified URL