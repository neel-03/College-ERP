from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, reverse

from main_app.models import Quiz, QuizResult, Response, Student, CustomUser

from .email_auth import backend


def login_user(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Acess denied!!</h2>')

    # authenticate user
    user = backend.CustomBackend.authenticate(
        username=request.POST.get('email'),
        password=request.POST.get('password')
    )

    if user is not None:
        login(request, user)
        return redirect('/')

    messages.error(request, "Invalid credentials")
    return redirect('/')

def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")


def login_page(request):
    if not request.user.is_authenticated:
        return render(request, 'common/login.html')

    match request.user.user_type:
        case '1':
            return redirect(reverse('hod_home'))
        case '2':
            return redirect(reverse('faculty_home'))
        case _:
            return redirect(reverse('student_home'))


def view_student_result(request, quiz_id, student_id):
    
    if request.user.user_type == 3:  # Student
        quiz = get_object_or_404(Quiz, id=quiz_id, is_result_declared=True)
    else:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
    student = get_object_or_404(Student, id=student_id)

    responses = Response.objects.filter(quiz=quiz, student=student).select_related('question')
    result = get_object_or_404(QuizResult, quiz=quiz, student=student)

    context = {
        'quiz': quiz,
        'student': student,
        'responses': responses,
        'result': result,
    }

    return render(request, 'common/student_result.html', context)