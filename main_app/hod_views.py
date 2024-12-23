import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *


def hod_home(request):
    return render(request, 'hod_templates/home_content.html')


def hod_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, instance=admin)

    context = {
        'form': form,
        'page_title': 'View / Edit Profile'
    }
    
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)

                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, 'Profile Updated!')
                return redirect(reverse('hod_view_profile'))
            else:
                messages.error(request, 'Invalid Data Provided')
        except Exception as e:
            messages.error(
                request, 'Error Occured While Updating Profile ' + str(e))
    return render(request, 'hod_templates/hod_view_profile.html', context)

def filter_faculties_by_course(request):
    course_id = request.GET.get('course_id')
    faculties = Faculty.objects.filter(course_id=course_id).values('id', 'admin__first_name', 'admin__last_name')
    return JsonResponse(list(faculties), safe=False)

def add_subject(request):
    course_id = request.GET.get('course_id')
    form = SubjectForm(request.POST or None, course_id=course_id)

    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            faculty = form.cleaned_data.get('faculty')  # queryset
            try:
                subject = Subject.objects.create(name=name, course=course)
                subject.faculty.set(faculty)
                subject.save()
                messages.success(request, 'Subject added successfully')
                return redirect(reverse('add_subject'))
            except Exception as e:
                messages.error(request, 'Could not add subject: ' + str(e))
        else:
            messages.error(request, 'Please fill in valid details')

    return render(request, 'hod_templates/add_subject_template.html', context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subjects'
    }
    return render(request, 'hod_templates/manage_subject.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)

    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'Edit Subject'
    }

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            faculties = form.cleaned_data.get('faculty')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.course = course
                subject.faculty.set(faculties)
                subject.save()

                messages.success(request, 'Subject updated successfully')
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, 'Could not update: ' + str(e))
        else:
            messages.error(request, 'Please fill in valid details')

    return render(request, 'hod_templates/edit_subject_template.html', context)


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject deleted successfully')
    return redirect(reverse('manage_subject'))


def add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                course = Course()
                course.name = name
                course.save()
                messages.success(request, 'Course added successfully')
                return redirect(reverse('add_course'))
            except:
                messages.error(request, 'Could tot add course')
        else:
            messages.error(request, 'Could tot add course')
    return render(request, 'hod_templates/add_course_template.html', context)


def manage_course(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'page_title': 'Manage Courses'
    }
    return render(request, 'hod_templates/manage_course.html', context)


def edit_course(request, course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'course_id': course_id,
        'page_title': 'Edit Course'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                course = Course.objects.get(id=course_id)
                course.name = name
                course.save()
                messages.success(request, 'Course updated successfully')
            except:
                messages.error(request, 'Could not update course')
        else:
            messages.error(request, 'Could Not Update course')

    return render(request, 'hod_templates/edit_course_template.html', context)


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    try:
        course.delete()
        messages.success(request, 'Course deleted successfully')
    except Exception:
        messages.error(request, 'Some students are assigned to this course already.')
    return redirect(reverse('manage_course'))


def add_batch(request):
    form = BatchForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Batch'}

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Batch created Successfully")
                return redirect(reverse('add_batch'))
            except Exception as e:
                messages.error(request, f"Could not create batch: {str(e)}")
        else:
            messages.error(request, "Please fill the form correctly.")

    return render(request, "hod_templates/add_batch_template.html", context)


def manage_batch(request):
    batches = Batch.objects.all()
    context = {
        'batches': batches,
        'page_title': 'Manage Batch' 
    }

    return render(request, 'hod_templates/manage_batch.html', context)


def edit_batch(request, batch_id):
    instance = get_object_or_404(Batch, id=batch_id)
    form = BatchForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'batch_id': batch_id,
        'page_title': 'Edit Batch'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Batch Updated")
                return redirect(reverse('edit_batch', args=[batch_id]))
            except Exception as e:
                messages.error(
                    request, "Batch could not be updated " + str(e))
                return render(request, "hod_templates/edit_batch_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_templates/edit_batch_template.html", context)

    else:
        return render(request, "hod_templates/edit_batch_template.html", context)
    

def delete_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    try:
        batch.delete()
        messages.success(request, "Batch deleted successfully!")
    except Exception:
        messages.error(request, "There are students assigned to this batch.")
    return redirect(reverse('manage_batch'))


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


def add_faculty(request):
    form = FacultyForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Faculty'
    }

    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')

            try:
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    user_type='2',
                    gender=gender,
                )

                Faculty.objects.create(
                    admin=user,
                    course=course
                )

                messages.success(request, "Faculty added successfully")
                return redirect(reverse('add_faculty'))

            except Exception as e:
                messages.error(request, "Could not add faculty: " + str(e))
        else:
            messages.error(request, "Please fill all the details")
    return render(request, 'hod_templates/add_faculty_template.html', context)


def manage_faculty(request):
    all_faculties = CustomUser.objects.filter(user_type='2')
    context = {
        'all_faculties': all_faculties,
        'page_title' : 'Manage Faculties'
    }
    return render(request, 'hod_templates/manage_faculty.html', context) 


def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    form = FacultyForm(request.POST or None, instance=faculty)
    context = {
        'form': form,
        'faculty_id': faculty_id,
        'page_title': 'Edit Faculty'
    }

    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')

            try:
                user = CustomUser.objects.get(id=faculty.admin.id)

                user.username = username
                user.email = email
                if password:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.save() 
                
                faculty.course = course
                faculty.save()

                messages.success(request, "Faculty updated successfully")
                return redirect(reverse('edit_faculty', args=[faculty_id]))

            except Exception as e:
                messages.error(request, f"Could not update faculty: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")

    return render(request, "hod_templates/edit_faculty_template.html", context)


def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(CustomUser, faculty__id=faculty_id)
    faculty.delete()
    messages.success(request, "faculty deleted successfully!")
    return redirect(reverse('manage_faculty'))


def add_student(request):
    form = StudentForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Student'
    }

    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            batch = form.cleaned_data.get('batch')

            try:
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    user_type='3',
                    gender=gender,
                )

                Student.objects.create(
                    admin=user,
                    course=course,
                    batch=batch
                )

                messages.success(request, "Student added successfully")
                return redirect(reverse('add_student'))

            except Exception as e:
                messages.error(request, "Could not add student: " + str(e))
        else:
            messages.error(request, "Please fill all the details")
    return render(request, 'hod_templates/add_student_template.html', context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'faculty_id': student_id,
        'page_title': 'Edit Student'
    }

    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            batch = form.cleaned_data.get('batch')

            try:
                user = CustomUser.objects.get(id=student.admin.id)

                user.username = username
                user.email = email
                if password:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.save()

                student.course = course
                student.batch = batch
                student.save()

                messages.success(request, "Student updated successfully")
                return redirect(reverse('edit_student', args=[student_id]))

            except Exception as e:
                messages.error(request, f"Could not update student: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")

    return render(request, "hod_templates/edit_student_template.html", context)


def manage_student(request):
    all_students = CustomUser.objects.filter(user_type='3')
    context = {
        'all_students': all_students,
        'page_title': 'Manage Student'
    }
    return render(request, 'hod_templates/manage_student.html', context)

def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))


@csrf_exempt
def view_faculty_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportFaculty.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Faculty'
        }
        return render(request, "hod_templates/faculty_leave_view.html", context)

    try:
        data = json.loads(request.body)
        leave_id = data.get('id')
        status = data.get('status')
        status = 1 if status == '1' else -1

        leave = get_object_or_404(LeaveReportFaculty, id=leave_id)
        leave.status = status
        leave.save()

        return HttpResponse("True")
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_student_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Student'
        }
        return render(request, "hod_templates/student_leave_view.html", context)

    try:
        data = json.loads(request.body)
        leave_id = data.get('id')
        status = data.get('status')
        status = 1 if status == '1' else -1

        leave = get_object_or_404(LeaveReportStudent, id=leave_id)
        leave.status = status
        leave.save()

        return HttpResponse("True")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
