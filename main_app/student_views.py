from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from random import shuffle

from .forms import *
from .models import *


def student_home(request):
    student = get_object_or_404(Student, admin=request.user)
    
    all_faculties_count = Faculty.objects.filter(course=student.course).count()
    
    all_student_quizzes = Quiz.objects.filter(
        batch=student.batch, 
        subject__course=student.course
    )
    attempted_quiz_ids = QuizResult.objects.filter(
        student=student
    ).values_list('quiz', flat=True)
    
    # Annotate quiz counts
    missed_quizzes_count = all_student_quizzes.filter(
        status='closed'
    ).exclude(
        id__in=attempted_quiz_ids
    ).count()
    
    pending_quizzes_count = all_student_quizzes.filter(
        status='active'
    ).exclude(
        id__in=attempted_quiz_ids
    ).count()
    
    # Get leave data
    current_year = datetime.now().year
    current_year_leaves = LeaveReportStudent.objects.filter(
        student=student,
        created_at__year=current_year
    )
    
    # Calculate month-wise leaves
    month_wise_leaves = [0] * 12
    for leave in current_year_leaves:
        month_wise_leaves[leave.created_at.month - 1] += 1
    
    total_leaves = LeaveReportStudent.objects.filter(student=student).count()
    
    context = {
        'page_title': f'Student Panel - {student.admin.first_name} {student.admin.last_name} ({student.course})',
        'student_course': student.course,
        'student_batch': student.batch,
        'total_faculties': all_faculties_count,
        'missed_quizzes': missed_quizzes_count,
        'pending_quizzes': pending_quizzes_count,
        'attempted_quizzes': QuizResult.objects.filter(student=student).count(),
        'total_quizzes': all_student_quizzes.count(),
        'total_leaves': total_leaves,
        'month_wise_leaves': month_wise_leaves,
    }
    
    return render(request, 'student_templates/home_content.html', context=context)


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
    student_course_admin = get_object_or_404(Course, id=request.user.student.course.id).admin
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
                obj.requested_to = student_course_admin
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
        batch=student.batch, 
        subject__course=student.course
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
    if QuizResult.objects.filter(student=student, quiz_id=quiz_id).exists():
        messages.info(request, "You have already attempted this quiz.")
        return redirect('student_view_quiz')

    quiz = get_object_or_404(Quiz, id=quiz_id, status='active')
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


def view_all_faculties(request):
    student = get_object_or_404(Student, admin=request.user)
    faculties = Faculty.objects.filter(course=student.course).prefetch_related('subjects')

    faculty_data = []
    for faculty in faculties:
        faculty_subjects = faculty.subjects.filter(course=student.course)
        faculty_data.append({
            'faculty': faculty,
            'subjects': faculty_subjects
        })

    context = {
        'page_title': f'View All Faculties: ({student.course})',
        'faculty_data': faculty_data,
    }

    return render(request, 'student_templates/view_all_faculties.html', context=context)
