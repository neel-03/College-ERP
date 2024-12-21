from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect

class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        requested_module = view_func.__module__
        curr_user = request.user
        
        if curr_user.is_authenticated:
            match curr_user.user_type:
                case '1': # admin/HOD
                    # hods are not allowed to access student views
                    if requested_module == 'main_app.student_views': 
                        return redirect(reverse('hod_home'))
                
                case '2': # faculty
                    # faculties are not allowed to access student and admin views
                    if requested_module == 'main_app.student_views' or requested_module == 'main_app.hod_views':
                        return redirect(reverse('faculty_home'))
                    
                case '3': # students
                    # students are not allowed to access faculty and admin views
                    if requested_module == 'main_app.hod_views' or requested_module == 'main_app.staff_views':
                        return redirect(reverse('student_home'))
                    
                case _:
                    print('going')
                    return redirect(reverse('login_page'))

        else: # user not authenticated
            allowed_paths = [ # allowed paths for unauthenticated users
                reverse('login_page'),
                reverse('login_user'),
            ]

            if request.path in allowed_paths or requested_module == 'django.contrib.auth.views':
                pass
            else:
                return redirect(reverse('login_page'))




