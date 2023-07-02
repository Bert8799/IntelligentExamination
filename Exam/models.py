from django.db import models
from Student.models import Student


# Create your models here.


# 考试
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   date = models.DateTimeField(auto_now=True)

   def __str__(self):
        return self.course_name


# 问题（单选题）
class Question(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)

    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)

    cat=(('A', '选项A'), ('B', '选项B'), ('C', '选项C'), ('D', '选项D'))
    
    answer=models.CharField(max_length=200, choices=cat)


class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
