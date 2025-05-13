from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from student.models import User
from student.models import StudentProfile
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.timezone import localtime
from authentication.tasks import schedule_account_deletion

# Create your views here.

def home(request):
    return redirect('login/')

def login_fun(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        mentor_login = request.POST.get('mentorLogin')  # Check if the checkbox is selected

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if mentor_login:  # If the checkbox is selected
                # Check if the user is a mentor (you may need a MentorProfile model or a flag in the User model)
                if hasattr(user, 'mentorprofile'):  # Example check for a MentorProfile
                    login(request, user)
                    # messages.success(request, "Mentor login successful!")
                    return redirect('mentorhome')  # Redirect to the mentor page
                else:
                    messages.error(request, "You are not registered as a mentor.")
                    return redirect('login')
            else:
                if hasattr(user, 'studentprofile'):  # Example check for a StudentProfile
                    profile = StudentProfile.objects.get(user=user)
                    if profile.is_verified:
                        if not profile.is_approved:
                            messages.error(request, "Your account is not approved yet. Please wait for admin approval.")
                            return redirect('login')
                        else:
                            login(request, user)
                            return redirect('home')  # Redirect to the home page
                    else:
                        messages.error(request, "Your email is not verified. Please verify your email.")
                        return redirect('login')
                
                elif not hasattr(user, 'studentprofile') and not hasattr(user, 'mentorprofile'):
                    login(request, user)
                    return redirect('admin_home') # Redirect to admin home if the user is neither a student nor a mentor
                else:
                    messages.error(request, "User profile not found. Please contact support.")
                    return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')

def register_fun(request):
    if request.method == 'POST':
        try:
            college_id = request.FILES['image']  # Handle file upload
        except MultiValueDictKeyError:
            college_id = None  # Handle the case where no file is uploaded

        # Extract form data
        name = request.POST['name']
        college = request.POST['college']
        mobile = request.POST['mobile']
        branch = request.POST['branch']
        enrollment_number = request.POST['enrollment']
        year_of_study = request.POST['year']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check for duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use a different email")
            return render(request, 'register.html')

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose a different username")
            return render(request, 'register.html')

        # Check for duplicate enrollment number
        if StudentProfile.objects.filter(enrollment_number=enrollment_number).exists():
            messages.error(request, "Enrollment number is already registered. Please use a different enrollment number")
            return render(request, 'register.html')

        # Hash the password
        hashed_password = make_password(password)

        # Save the user
        user = User.objects.create(
            username=username,
            password=hashed_password,  # Store hashed password
        )

        user.save()
        pfp = StudentProfile.objects.create(
            user=user,
            name=name,
            email=email,
            college=college,
            mobile=mobile,
            branch=branch,
            enrollment_number=enrollment_number,
            year_of_study=year_of_study,
            college_id=college_id,
            is_verified=False,
            verification_code=str(random.randint(100000, 999999)),
        )

        pfp.save()

        # Send verification email
        # subject = 'Email Verification'
        # message = f'Your verification code is {pfp.verification_code}'
        # from_email = 'noreply@example.com'
        # recipient_list = [email]
        # send_mail(subject, message, from_email, recipient_list)

        
        schedule_account_deletion.apply_async((user.id,), countdown=60)
        print(f"Created at: {localtime(pfp.created_at)}")
        messages.success(request, "Registration successful! Please verify your email")
        return redirect('/auth/verify_email/')
    return render(request, 'register.html')

def logout_fun(request):
    logout(request)
    messages.error(request, "You have been logged out")
    return redirect('/auth/login/')


def verify_email(request):
    if request.method == 'POST':
        code = request.POST['code']
        try:
            profile = StudentProfile.objects.get(verification_code=code)
            profile.is_verified = True
            profile.verification_code = None  # Flush the verification code
            profile.save()
            messages.success(request, "Your email has been successfully verified!")
            messages.success(request, "Wait for admin approval")
            return redirect('login')  # Redirect to the login page or another page
        except StudentProfile.DoesNotExist:
            messages.error(request, "Invalid verification code")
            return redirect('verify_email')  # Redirect back to the verification page
    return render(request, 'verify_email.html')
