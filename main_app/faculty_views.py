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

