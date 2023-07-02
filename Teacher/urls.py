from django.urls import path
from Teacher import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('teacher_view', views.teacher_view),
    path('teacher_login', LoginView.as_view(template_name='teacher/teacher_login.html'),name='teacher_login'),
    path('teacher_signup', views.teacher_signup,name='teacher_signup'),

    path('teacher-dashboard', views.teacher_dashboard,name='teacher-dashboard'),


    path('teacher-exam', views.teacher_exam,name='teacher-exam'),
    path('teacher-exam-add', views.teacher_exam_add,name='teacher-exam-add'),
    path('teacher-exam-view', views.teacher_exam_view,name='teacher-exam-view'),
    path('teacher-exam-delete/<int:pk>', views.exam_delete,name='teacher-exam-delete'),


    path('teacher-question', views.teacher_question,name='teacher-question'),
    path('teacher-question-add', views.teacher_question_add,name='teacher-question-add'),
    path('teacher-question-view', views.teacher_question_view,name='teacher-question-view'),
    path('teacher-question-see/<int:pk>', views.question_see,name='teacher-question-see'),
    path('teacher-question-delete/<int:pk>', views.question_delete,name='teacher-question-delete'),
]