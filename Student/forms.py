from django import forms
from . import models
from django.contrib.auth.models import User


# 学生用户表单
class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }


# 学生信息表单
class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = ['student_id', 'student_name', 'mobile', 'profile_img']
