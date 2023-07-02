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
@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    dict={
        'total_course':QMODEL.Course.objects.all().count(),
        'total_question':QMODEL.Question.objects.all().count(),
        'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context={'dict':dict})


# 考试管理
@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_exam(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_exam_add(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            if QMODEL.Course.objects.filter(course_name=courseForm.cleaned_data['course_name']).exists():     
                messages.info(request, "考试类型已存在")
            else:
                courseForm.save()
                messages.info(request, "考试添加成功")
        return redirect('teacher-exam-add')
    return render(request,'teacher/teacher_exam_add.html',{'courseForm':courseForm})


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_exam_view.html',{'courses':courses})


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def exam_delete(request, pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    messages.info(request, "考试删除成功")
    return redirect('teacher-exam-view')


# 试题管理
@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_question(request):
    return render(request,'teacher/teacher_question.html')


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_question_add(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
            messages.info(request, "试题添加成功")
        else:
            messages.info(request, "试题已存在或考试类型不存在")
        return redirect('teacher-question-add')
    return render(request,'teacher/teacher_question_add.html',{'questionForm':questionForm})


# 查看全部试题
@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def teacher_question_view(request):
    courses= QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_question_view.html',{'courses':courses})


# 查看特定试题
@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def question_see(request, pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/teacher_question_see.html',{'questions':questions})


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher)
def question_delete(request, pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return redirect('teacher-question-view')
