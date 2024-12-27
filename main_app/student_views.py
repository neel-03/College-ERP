from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from random import shuffle

from .forms import *
from .models import *


def student_home(request):
    return render(request, 'student_templates/home_content.html')


def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(request.POST or None, instance=student)

    context = {
        'form': form,
        'page_title': 'View / Edit Profile'
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password') or None
                custom_user = student.admin
                if password != None:
                    custom_user.set_password(password)

                custom_user.email = email
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                student.save()
                messages.success(request, 'Profile Updated!')
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, 'Invalid Data Provided')
        except Exception as e:
            messages.error(
                request, 'Error Occured While Updating Profile: ' + str(e))
    return render(request, 'student_templates/student_view_profile.html', context)


def student_apply_leave(request):
    form = LeaveReportStudentForm(request.POST or None)
    student = get_object_or_404(Student, admin=request.user.id)

    context = {
        'form': form,
        'page_title': 'Apply for Leave',
        'leave_history': LeaveReportStudent.objects.filter(student=student)
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(request, "Application for leave has been submitted.")
                return redirect(reverse('student_apply_leave'))
            except Exception as e:
                messages.error(request, f"Could not apply for leave!{e}")
        else:
            messages.error(request, "Please fill valid details")
    return render(request, "student_templates/student_apply_leave.html", context)


def student_view_quiz(request):
    student = get_object_or_404(Student, admin=request.user)
    quizzes = Quiz.objects.filter(
        batch=student.batch
    ).annotate(
        attempted = models.Exists(
            Response.objects.filter(student=student, quiz=models.OuterRef('id'))
        )
    ).order_by(
        models.Case(
            models.When(status='active', then=0),
            models.When(status='closed', then=1),
            default=2
        ),
        'created_at'
    )
    context = {
        'quizzes': quizzes,
        'page_title': 'Quizzes'
    }
    return render(request, 'student_templates/student_view_quizzes.html', context)


def attempt_quiz(request, quiz_id):
    student = get_object_or_404(Student, admin=request.user)
    if QuizResult.objects.filter(student=student, quiz_id=quiz_id).exists():
        messages.info(request, "You have already attempted this quiz.")
        return redirect('student_view_quiz')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())

    shuffled_questions = []
    for question in questions:
        options = [question.correct_answer, question.option_1, question.option_2, question.option_3]
        shuffle(options)
        shuffled_questions.append({
            'id': question.id,
            'text': question.text,
            'options': options,
            'marks': question.marks
        })

    context = {
        'quiz': quiz,
        'questions': shuffled_questions,
        'page_title': f'Attempt Quiz: {quiz.name}'
    }

    return render(request, 'student_templates/student_attempt_quiz.html', context)


def submit_quiz(request, quiz_id):
    student = get_object_or_404(Student, admin=request.user)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        try:
            total_marks = 0
            for question in questions:
                selected_answer = request.POST.get(f'question_{question.id}')
                correct_answer = question.correct_answer

                if selected_answer:
                    is_correct = (selected_answer == correct_answer)
                    obtained_marks = question.marks if is_correct else 0
                    total_marks += obtained_marks
                    Response.objects.create(
                        student=student,
                        quiz=quiz,
                        question=question,
                        selected_answer=selected_answer,
                        is_correct=is_correct
                    )
            QuizResult.objects.create(
                student=student,
                quiz=quiz,
                total_marks=quiz.total_marks,
                obtained_marks=total_marks
            )
            return HttpResponse("True")
        except:
            return HttpResponse("False")    
    return redirect('student_view_quiz')



def view_result(request, quiz_id):
    return None