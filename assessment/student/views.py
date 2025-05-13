from django.shortcuts import render
from .models import StudentProfile, StudentSession, StudentAnswer  # Import your profile model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from announcements_manager.models import Announcements
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from community_manager.models import CommunityPost, CommunityReply  # Add this import
from django.template.loader import render_to_string
from testportal.models import Test  # Import your test model

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
    if hasattr(request.user, 'studentprofile'):
        pass
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
    if hasattr(request.user, 'studentprofile'):
        announs = Announcements.objects.all().order_by('-created_at')
        return render(request, 'announcements.html', {'announs': announs})
    else:
        messages.error(request, "Only students can access this page.")
        return render(request, 'announcements.html')

@login_required(login_url='/auth/login/')
def community(request):
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
        community = profile.community
        if request.method == 'POST':
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Handle reply
                if 'reply' in request.POST and 'doubt_id' in request.POST:
                    reply_content = request.POST.get('reply')
                    doubt_id = request.POST.get('doubt_id')
                    if reply_content and doubt_id:
                        try:
                            post = CommunityPost.objects.get(id=doubt_id)
                            reply = CommunityReply.objects.create(
                                post=post,
                                author=request.user,
                                content=reply_content
                            )
                            html = render_to_string('partials/reply.html', {'reply': reply})
                            return JsonResponse({'status': 'ok', 'html': html})
                        except CommunityPost.DoesNotExist:
                            return JsonResponse({'status': 'error'})
                # Handle new post
                elif 'content' in request.POST:
                    content = request.POST.get('content')
                    if community and content:
                        doubt = CommunityPost.objects.create(author=request.user, content=content)
                        html = render_to_string('partials/doubt.html', {'doubt': doubt})
                        return JsonResponse({'status': 'ok', 'html': html})
                return JsonResponse({'status': 'error'})
            else:
                # Handle regular POST (non-AJAX)
                if 'reply' in request.POST and 'doubt_id' in request.POST:
                    reply_content = request.POST.get('reply')
                    doubt_id = request.POST.get('doubt_id')
                    if reply_content and doubt_id:
                        try:
                            post = CommunityPost.objects.get(id=doubt_id)
                            CommunityReply.objects.create(
                                post=post,
                                author=request.user,
                                content=reply_content
                            )
                        except CommunityPost.DoesNotExist:
                            pass
                elif 'content' in request.POST:
                    content = request.POST.get('content')
                    if community and content:
                        CommunityPost.objects.create(author=request.user, content=content)
        # Refresh the list after post/reply
        doubts = CommunityPost.objects.select_related('author').prefetch_related('replies__author').order_by('-created_at')
        return render(request, 'community.html', {
            'community': community,
            'doubts': doubts,
        })
    else:
        messages.error(request, "Only students can access this page.")
    return render(request, 'community.html')


@csrf_exempt
@login_required
def accept_community_rules(request):
    if request.method == "POST":
        # Set user profile/community flag to True
        request.user.studentprofile.community = True
        request.user.studentprofile.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)