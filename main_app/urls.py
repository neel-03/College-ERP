from django.urls import path
from . import views, hod_views, faculty_views, student_views


urlpatterns = [
    path('', view=views.login_page, name='login_page'),


    path('login_user/', view=views.login_user, name='login_user'),
    path('logout_user/', view=views.logout_user, name='logout_user'),

    path('quiz/<int:quiz_id>/<int:student_id>/response/', view=views.view_student_result, name='view_student_result'),

    path('check_email_availability/', hod_views.check_email_availability, name='check_email_availability'),


    # HOD routes
    path('hod/home/', view=hod_views.hod_home, name='hod_home'),
    path('hod/profile/', view=hod_views.hod_view_profile, name='hod_view_profile'),

    path('hod/course/add/', view=hod_views.add_course, name='add_course'),
    path('hod/course/manage/', view=hod_views.manage_course, name='manage_course'),
    path('hod/course/<int:course_id>/edit/', view=hod_views.edit_course, name='edit_course'),
    path('hod/course/<int:course_id>/delete/', view=hod_views.delete_course, name='delete_course'),

    path('hod/batch/add/', view=hod_views.add_batch, name='add_batch'),
    path('hos/batch/manage/', view=hod_views.manage_batch, name='manage_batch'),
    path('hod/batch/<int:batch_id>/edit/', view=hod_views.edit_batch, name='edit_batch'),
    path('hod/batch/<int:batch_id>/delete/', view=hod_views.delete_batch, name='delete_batch'),

    path('filter-faculties-by-course/', view=hod_views.filter_faculties_by_course, name='filter_faculties_by_course'),

    path('hod/subject/add/', view=hod_views.add_subject, name='add_subject'),
    path('hod/subject/manage/', view=hod_views.manage_subject, name='manage_subject'),
    path('hod/subject/<int:subject_id>/edit/', view=hod_views.edit_subject, name='edit_subject'),
    path('hod/subject/<int:subject_id>/delete/', view=hod_views.delete_subject, name='delete_subject'),

    path('hod/faculty/add/', hod_views.add_faculty, name='add_faculty'),
    path('hod/faculty/manage/', view=hod_views.manage_faculty, name='manage_faculty'),
    path('hod/faculty/<int:faculty_id>/edit/', view=hod_views.edit_faculty, name='edit_faculty'),
    path('hod/faculty/<int:faculty_id>/delete/', view=hod_views.delete_faculty, name='delete_faculty'),

    path('hod/student/add/', hod_views.add_student, name='add_student'),
    path('hod/student/manage/', view=hod_views.manage_student, name='manage_student'),
    path('hod/student/<int:student_id>/edit/', view=hod_views.edit_student, name='edit_student'),
    path('hod/student/<int:student_id>/delete/', view=hod_views.delete_student, name='delete_student'),

    path('faculty/view/leave/', hod_views.view_faculty_leave, name='view_faculty_leave'),
    path('student/view/leave/', hod_views.view_student_leave, name='view_student_leave'),


    # Faculty routes
    path('faculty/home/', view=faculty_views.faculty_home, name='faculty_home'),
    path('faculty/home/subjects/all/', view=faculty_views.view_all_subjects, name='view_all_subjects'),
    path('faculty/home/batch/all/', view=faculty_views.view_all_batches, name='view_all_batches'),
    path('faculty/home/batch/<int:batch_id>/', view=faculty_views.view_students_in_batch, name='view_students_in_batch'),
    
    path('faculty/profile/', view=faculty_views.faculty_view_profile, name='faculty_view_profile'),

    path('faculty/leave/', faculty_views.faculty_apply_leave, name='faculty_apply_leave'),

    path('faculty/quiz/create/', view=faculty_views.faculty_create_quiz, name='faculty_create_quiz'),
    path('faculty/quiz/<int:quiz_id>/delete/', view=faculty_views.faculty_delete_quiz, name='faculty_delete_quiz'),
    path('faculty/quiz/<int:quiz_id>/toggle/<str:field>', view=faculty_views.faculty_toggle_quiz, name='faculty_toggle_quiz'),
    path('faculty/quiz/<int:quiz_id>/responses/', view=faculty_views.faculty_view_responses, name='faculty_view_responses'),
    path('faculty/questions/<int:quiz_id>/add/', view=faculty_views.faculty_add_questions, name='faculty_add_questions'),
    path('faculty/manage/quiz/', view=faculty_views.faculty_manage_quiz,name='faculty_manage_quiz'),


    # Student routes
    path('student/home/', view=student_views.student_home, name='student_home'),
    path('student/profile/', view=student_views.student_view_profile, name='student_view_profile'),
    path('student/leave/', student_views.student_apply_leave, name='student_apply_leave'),

    path('student/quiz/view/', view=student_views.student_view_quiz, name='student_view_quiz'),

    path('student/quiz/<int:quiz_id>/attempt/', view=student_views.attempt_quiz, name='attempt_quiz'),
    path('student/quiz/<int:quiz_id>/submit/', view=student_views.submit_quiz, name='submit_quiz'),
]
