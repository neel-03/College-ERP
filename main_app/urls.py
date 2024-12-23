from django.urls import path
from . import views, hod_views, faculty_views, student_views


urlpatterns = [
    path('', view=views.login_page, name='login_page'),


    path('login_user/', view=views.login_user, name='login_user'),
    path('logout_user/', view=views.logout_user, name='logout_user'),


    path('check_email_availability/', hod_views.check_email_availability, name='check_email_availability'),


    # HOD routes
    path('hod/home/', view=hod_views.hod_home, name='hod_home'),
    path('hod_view_profile/', view=hod_views.hod_view_profile, name='hod_view_profile'),

    path('add_course/', view=hod_views.add_course, name='add_course'),
    path('manage_course/', view=hod_views.manage_course, name='manage_course'),
    path('course/edit/<int:course_id>/', view=hod_views.edit_course, name='edit_course'),
    path('course/delete/<int:course_id>/', view=hod_views.delete_course, name='delete_course'),

    path('add_batch/', view=hod_views.add_batch, name='add_batch'),
    path('manage_batch/', view=hod_views.manage_batch, name='manage_batch'),
    path('batch/edit/<int:batch_id>/', view=hod_views.edit_batch, name='edit_batch'),
    path('batch/delete/<int:batch_id>/', view=hod_views.delete_batch, name='delete_batch'),

    path('filter-faculties-by-course/', view=hod_views.filter_faculties_by_course, name='filter_faculties_by_course'),

    path('add_subject/', view=hod_views.add_subject, name='add_subject'),
    path('manage_subject/', view=hod_views.manage_subject, name='manage_subject'),
    path('subject/edit/<int:subject_id>/', view=hod_views.edit_subject, name='edit_subject'),
    path('subject/delete/<int:subject_id>/', view=hod_views.delete_subject, name='delete_subject'),

    path('add_faculty/', hod_views.add_faculty, name='add_faculty'),
    path('manage_faculty/', view=hod_views.manage_faculty, name='manage_faculty'),
    path('faculty/edit/<int:faculty_id>/', view=hod_views.edit_faculty, name='edit_faculty'),
    path('faculty/delete/<int:faculty_id>/', view=hod_views.delete_faculty, name='delete_faculty'),

    path('add_student/', hod_views.add_student, name='add_student'),
    path('manage_student/', view=hod_views.manage_student, name='manage_student'),
    path('student/edit/<int:student_id>/', view=hod_views.edit_student, name='edit_student'),
    path('student/delete/<int:student_id>/', view=hod_views.delete_student, name='delete_student'),

    path("faculty/view/leave/", hod_views.view_faculty_leave, name="view_faculty_leave"),
    path("student/view/leave/", hod_views.view_student_leave, name="view_student_leave"),


    # Faculty routes
    path('faculty/home/', view=faculty_views.faculty_home, name='faculty_home'),
    path('faculty_view_profile/', view=faculty_views.faculty_view_profile, name='faculty_view_profile'),

    path("faculty_apply_leave/", faculty_views.faculty_apply_leave, name='faculty_apply_leave'),


    # Student routes
    path('student/home/', view=student_views.student_home, name='student_home'),
    path('student_view_profile/', view=student_views.student_view_profile, name='student_view_profile'),
    path("student_apply_leave/", student_views.student_apply_leave, name='student_apply_leave'),
]
