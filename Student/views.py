from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from Exam import models as QMODEL

# Create your views here.


# 学生欢迎页
def student_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'student/student_view.html')


# 学生注册页
def student_signup(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    forms_dict={'userForm':userForm,'studentForm':studentForm}

    if request.method == 'POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            student_group = Group.objects.get_or_create(name='STUDENT')
            student_group[0].user_set.add(user)
            return redirect('student_login')
        else:
            messages.info(request, "用户名已被注册")
            return redirect('student_signup')
    return render(request,'student/student_signup.html',context=forms_dict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='student_login')
@user_passes_test(is_student)
def student_dashboard(request):
    dict={
        'total_course':QMODEL.Course.objects.all().count(),
        'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context={'dict':dict})


# 我的考试
@login_required(login_url='student_login')
@user_passes_test(is_student)
def student_exam(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html', context={'courses':courses})


# 以下位考试与计算分数流程
@login_required(login_url='student_login')
@user_passes_test(is_student)
def exam_take(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request, 'student/student_exam_take.html', context={'course':course,'total_questions':total_questions,'total_marks':total_marks})


@login_required(login_url='student_login')
@user_passes_test(is_student)
def exam_start(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/student_exam_start.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='student_login')
@user_passes_test(is_student)
def exam_marks(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks

        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return redirect(f'student-marks-see/{course_id}')


@login_required(login_url='student_login')
@user_passes_test(is_student)
def exam_result(request):
    courses=QMODEL.Course.objects.all()
    return render(request, 'student/student_exam_result.html', context={'courses':courses})


# 我的分数
@login_required(login_url='student_login')
@user_passes_test(is_student)
def student_marks(request):
    courses=QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', context={'courses':courses})


@login_required(login_url='student_login')
@user_passes_test(is_student)
def marks_see(request, pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'student/student_marks_see.html', {'results':results})
