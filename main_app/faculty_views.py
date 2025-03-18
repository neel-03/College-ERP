import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .forms import *
from .models import *

def faculty_home(request):
    return render(request, 'faculty_templates/home_content.html')


def faculty_view_profile(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    form = FacultyEditForm(request.POST or None, instance=faculty)

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
                custom_user = faculty.admin
                if password != None:
                    custom_user.set_password(password)

                custom_user.email = email
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                faculty.save()
                messages.success(request, 'Profile Updated!')
                return redirect(reverse('faculty_view_profile'))
            else:
                messages.error(request, 'Invalid Data Provided')
        except Exception as e:
            messages.error(request, 'Error Occured While Updating Profile: ' + str(e))
    return render(request, 'faculty_templates/faculty_view_profile.html', context)


def faculty_apply_leave(request):
    faculty_course_admin = get_object_or_404(Course, id=request.user.faculty.course.id).admin
    form = LeaveReportFacultyForm(request.POST or None)
    faculty = get_object_or_404(Faculty, admin=request.user.id)

    context = {
        'form': form,
        'page_title': 'Apply for Leave',
        'leave_history': LeaveReportFaculty.objects.filter(faculty=faculty)
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.faculty = faculty
                obj.requested_to = faculty_course_admin
                obj.save()
                messages.success(request, "Application for leave has been submitted.")
                return redirect(reverse('faculty_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply for leave!")
        else:
            messages.error(request, "Please fill valid details")
    return render(request, "faculty_templates/faculty_apply_leave.html", context)


def faculty_create_quiz(request):
    form = QuizForm(request.POST or None, logged_in_user=request.user.faculty)

    context = {
        'form': form,
        'page_title': 'Create Quiz'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                quiz = form.save(commit=False)
                quiz.created_by = request.user.faculty
                quiz.save()
                return redirect(reverse('faculty_add_questions', args=[quiz.id]))
            except Exception as e:
                messages.error(request, f"Could not create quiz: {str(e)}")
        else:
            messages.error(request, "Please fill valid details")
    else:
        form = QuizForm(logged_in_user=request.user.faculty)
    return render(request, "faculty_templates/faculty_create_quiz.html", context)

def faculty_add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questions = data.get('questions', [])

            for question in questions:
                Question.objects.create(
                    quiz=quiz,
                    text=question['text'],
                    correct_answer=question['correct_answer'],
                    option_1=question['option_1'],
                    option_2=question['option_2'],
                    option_3=question['option_3'],
                    marks=question['marks'],
                )
            quiz.status = 'active'
            quiz.save()
            return HttpResponse('True')
        except Exception:
            return HttpResponse('False')

    return render(request, 'faculty_templates/faculty_add_questions.html', {'quiz': quiz, 'page_title': 'Add Questions'})


def faculty_manage_quiz(request):
    quizzes = Quiz.objects.filter(created_by=request.user.faculty)

    context = {
        'quizzes': quizzes,
        'page_title': 'Manage your Quizzes'
    }

    return render(request, 'faculty_templates/faculty_manage_quiz.html', context)


def faculty_edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user.faculty)
    form = QuizForm(request.POST or None, instance=quiz, logged_in_user=request.user.faculty)

    context = {
        'form': form,
        'page_title': 'Edit Quiz'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Quiz updated successfully.")
                return redirect(reverse('faculty_manage_quiz'))
            except Exception as e:
                messages.error(request, f"Could not update quiz: {str(e)}")
        else:
            messages.error(request, "Please fill valid details")
    return render(request, "faculty_templates/faculty_edit_quiz.html", context)


def faculty_delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user.faculty)
    try:
        quiz.delete()
        messages.success(request, "Quiz deleted successfully.")
    except Exception as e:
        messages.error(request, f"Could not delete quiz: {str(e)}")
    return redirect(reverse('faculty_manage_quiz'))


def faculty_toggle_quiz(request, quiz_id, field):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user.faculty)
    try:
        match field:
            case 'status':
                quiz.status = 'closed' if quiz.status == 'active' else 'active'
                quiz.save()
                messages.success(request, f"Quiz status changed to {quiz.status}.")
            case 'result':
                quiz.is_result_declared = not quiz.is_result_declared
                quiz.save()
                messages.success(request, f"Quiz result declaration for {quiz.name}: {'ON' if quiz.is_result_declared else 'OFF'}.")
            case _:
                raise ValueError(f"Invalid toggling for {field}.")
    except ValueError as ve:
        messages.error(request, f"Error: {str(ve)}")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
    return redirect(reverse('faculty_manage_quiz'))


def faculty_view_responses(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user.faculty)
    responses = Response.objects.filter(quiz=quiz)

    context = {
        'quiz': quiz,
        'responses': responses,
        'page_title': 'View Responses'
    }

    return render(request, 'faculty_templates/faculty_view_responses.html', context)