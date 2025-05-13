from django.shortcuts import render, redirect
from .models import Test, Question
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import json
from django.urls import reverse
from student.models import StudentSession, StudentAnswer
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
# Create your views here.

@login_required(login_url='/auth/login/')
def testlanding(request):
    if hasattr(request.user, 'mentorprofile'):
        test_code = request.POST.get('test_code') or request.GET.get('test_code')
        return render(request, 'livetestlanding.html', {'ismentor': True, 'test_code': test_code})
    elif hasattr(request.user, 'studentprofile'):
        if request.method == 'POST':
            test_code = request.POST.get('test_code')
            print(test_code)
            try:
                test = Test.objects.get(test_code=test_code)
                if test.active:
                    return render(request, 'livetestlanding.html', {'ismentor': False, 'test_code': test_code})
                else:
                    messages.error(request, "Test is not active")
            except Exception as e:
                messages.error(request, "Test not found")
        return redirect('/student/test/')
    else:
        return HttpResponse("You are not a mentor or student.")


# Add this new view
@login_required(login_url='/auth/login/')
def start_test(request):
    if hasattr(request.user, 'mentorprofile'):
        if request.method == 'POST':
            test_code = request.POST.get('test_code')
            try:
                test = Test.objects.get(test_code=test_code)
                if test.started:
                    # messages.success(request, 'Test is already started!')
                    print('Test is already started!')
                else:
                    test.started = True
                    test.start_time = datetime.now()
                    test.save()
                return redirect(f"{reverse('livetestportalpage')}?test_code={test_code}")
            except Exception as e:
                messages.error(request, "Test not found")
    else:
        messages.error(request, "Only mentors can access this page.")
    return redirect('take_test')


@login_required(login_url='/auth/login/')
def livetestportalpage(request):
    if hasattr(request.user, 'mentorprofile'):
        test_code = request.GET.get('test_code')
        test = Test.objects.get(test_code=test_code)
        return render(request, 'livetestportalpage.html', {
            'test': test, 
            'ismentor': True, 
            'start_time': test.start_time,
            'duration': test.duration_minutes,
            })
    elif hasattr(request.user, 'studentprofile'):
        test_code = request.GET.get('test_code') or request.POST.get('test_code')
        test = Test.objects.get(test_code=test_code)
        session, created = StudentSession.objects.get_or_create(
            student=request.user.studentprofile,
            test=test,
            defaults={'start_time': test.start_time}
        )
        # Randomize and save order only on first creation
        if created or not session.question_order:
            questions = list(Question.objects.filter(test=test))
            random.shuffle(questions)
            session.question_order = [q.id for q in questions]
            session.current_index = 0
            session.save()
        else:
            questions = list(Question.objects.filter(id__in=session.question_order))
            # Ensure order matches session.question_order
            questions.sort(key=lambda q: session.question_order.index(q.id))

        # Prepare JSON-safe question data (no correct_option_id)
        question_data = [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": [q.option_a, q.option_b, q.option_c, q.option_d]
            }
            for q in questions
        ]

        # Get answered questions and selected options
        answers = StudentAnswer.objects.filter(session=session)
        answered = {a.question.id: a.selected_option for a in answers if a.selected_option is not None}

        return render(request, 'livetestportalpage.html', {
            'test': test,
            'questions_json': json.dumps(question_data),
            'answered': json.dumps(answered),  # {question_id: selected_option_index}
            'current_index': session.current_index,
            'session_id': session.id,
            'ismentor': False,
            'start_time': test.start_time,
            'duration': test.duration_minutes,
        })
    else:
        messages.error(request, "Only mentors can access this page.")
    return render(request, 'livetestportalpage.html')




@login_required(login_url='/auth/login/')
def active_test(request):
    if hasattr(request.user, 'mentorprofile'):
        if request.method == 'POST':
            test_code = request.POST.get('test_code')
            try:
                test = Test.objects.get(test_code=test_code)

                if test.started:
                    messages.success(request, 'Test is started already !')
                elif test.active == False:
                    test.active = True
                    test.save()
                    return redirect(f"{reverse('testlanding')}?test_code={test_code}")
            except Exception as e:
                messages.success(request, "Test not found")
    else:
        messages.error(request, "Only mentors can access this page.")
    return redirect('take_test')




@csrf_exempt
@login_required(login_url='/auth/login/')
def submit_answer(request):
    option = ['A', 'B', 'C', 'D']
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')
        session = StudentSession.objects.get(id=session_id, student=request.user.studentprofile)
        question = Question.objects.get(id=question_id)
        answer, created = StudentAnswer.objects.get_or_create(session=session, question=question)
        answer.selected_option = option[selected_option]
        # Optionally, validate answer here
        if question.correct_option_id == answer.selected_option:
            answer.is_correct = True
        else:
            answer.is_correct = False
        answer.save()
        # Update progress if needed
        if session.current_index < len(session.question_order) - 1:
            session.current_index += 1
            session.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required(login_url='/auth/login/')
def check_test_started(request, test_code):
    try:
        test = Test.objects.get(test_code=test_code)
        return JsonResponse({'started': test.started})
    except Test.DoesNotExist:
        return JsonResponse({'started': False})
    

@login_required(login_url='/auth/login/')
@csrf_exempt
def end_test(request):
    if hasattr(request.user, 'studentprofile'):
        if request.method == 'POST':
            data = json.loads(request.body)
            test_code = data.get('test_code')
            try:
                test = Test.objects.get(test_code=test_code)
                st_session = StudentSession.objects.get(student=request.user.studentprofile, test=test)
                st_session.submitted_at = timezone.now()
                st_session.completed = True
                st_session.current_index = st_session.current_index + 1
                st_session.save()
                return JsonResponse({'status': 'ok'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only students can end test.'}, status=403)