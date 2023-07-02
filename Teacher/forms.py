from django import forms
from django.contrib.auth.models import User
from . import models


class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets = {
            'password': forms.PasswordInput()
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields=['teacher_id','teacher_name', 'mobile','profile_img']

