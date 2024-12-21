from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, reverse

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
