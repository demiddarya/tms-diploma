from time import gmtime, strftime
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from byticket.forms import LoginForm, RegistrationForm
from byticket.models import User


# Create your views here.
def welcome_request(request: HttpResponse):
    return render(request, 'byticket/welcome.html')


def login_request(request: HttpResponse):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                print(f'User from DB: {user}')
                # TODO: fix this shit
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    return redirect('/home')
                else:
                    form.add_error('password', 'Invalid password')

            except User.DoesNotExist:
                # If the user does not exist, add an error message to the form.
                form.add_error('username', 'User does not exist')

    else:
        form = LoginForm()

    return render(request, 'byticket/login.html', {'form': form})


def register_request(request: HttpResponse):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            created_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            user = User.objects.create(username=username, email=email, password=password, created_at=created_at)
            print(f'User info: \n\t{user}')
            user.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    return render(request, 'byticket/register.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/welcome")


# @login_required
def home_request(request: HttpResponse):
    return render(request, 'byticket/home.html')
