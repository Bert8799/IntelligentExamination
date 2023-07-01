from django.shortcuts import render, redirect
from . import forms, models


# Create your views here.


# 默认页
def home(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')  
    return render(request,'exam/index.html')


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()