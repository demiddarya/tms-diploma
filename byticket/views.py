from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def welcome(request: HttpResponse):
    return render(request, 'byticket/base.html')


def auth(request: HttpResponse):
    return render(request, 'byticket/auth.html')


def register(request: HttpResponse):
    return render(request, 'byticket/register.html')
