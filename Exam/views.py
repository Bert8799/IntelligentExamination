from django.shortcuts import render, redirect
from . import forms, models
from Teacher import models as TMODEL
from Student import models as SMODEL
from Teacher import forms as TFORM
from Student import forms as SFORM
from django.contrib.auth.models import User


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


def afterlogin(request):
    if is_student(request.user):
        return redirect('student/student-dashboard')
    
    elif is_teacher(request.user):
        # 教师是否可见
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')
    

def admin_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return redirect('adminlogin')
