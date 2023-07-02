from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from Exam import models as QMODEL
from Student import models as SMODEL
from Exam import forms as QFORM

# Create your views here.


# 教师欢迎页
def teacher_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request,'teacher/teacher_view.html')


# 教师注册页
def teacher_signup(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    forms_dict={'userForm':userForm,'teacherForm':teacherForm}

    if request.method == 'POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            teacher_group = Group.objects.get_or_create(name='TEACHER')
            teacher_group[0].user_set.add(user)
            return redirect('teacher_login')
        else:
            messages.info(request, "用户名已被注册")
            return redirect('teacher_signup')
    return render(request,'teacher/teacher_signup.html',context=forms_dict)


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


# 详情页
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    dict={
        'total_course':QMODEL.Course.objects.all().count(),
        'total_question':QMODEL.Question.objects.all().count(),
        'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context={'dict':dict})


# 考试管理
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_add(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
            messages.info(request, "考试添加成功")
        else:
            messages.info(request, "考试已存在")
        return redirect('teacher-exam-add')
    return render(request,'teacher/teacher_exam_add.html',{'courseForm':courseForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_exam_view.html',{'courses':courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def exam_delete(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return redirect('teacher-exam-view')


# 试题管理
@login_required(login_url='adminlogin')
@user_passes_test(is_teacher)
def teacher_question(request):
    return render(request,'teacher/teacher_question.html')

