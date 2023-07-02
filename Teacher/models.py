from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20)
    teacher_name = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='profile_img/Teacher/', null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)

    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)

    @property
    def get_name(self) -> str:
        return self.teacher_name
    
    @property
    def get_instance(self):
        return self
    
    def __str__(self) -> str:
        return self.teacher_id+' '+self.teacher_name