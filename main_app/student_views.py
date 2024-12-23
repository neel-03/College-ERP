from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

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
