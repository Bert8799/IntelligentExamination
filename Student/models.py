from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='profile_img/Student/', null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)

    # 创建只读属性
    @property
    def get_name(self) -> str:
        return self.student_name

    @property
    def get_instance(self):
        return self
    
    def __str__(self) -> str:
        return self.student_id+' '+self.student_name