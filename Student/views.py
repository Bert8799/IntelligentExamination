from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import Group

# Create your views here.


# 学生欢迎页
def student_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'student/student_view.html')


# 学生注册页
def stduent_signup(request):
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
    
    return render(request,'student/student_signup.html',context=forms_dict)