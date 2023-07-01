from django.urls import path
from Student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('student_view', views.student_view),
    path('student_login', LoginView.as_view(template_name='student/student_login.html'),name='student_login'),
    path('student_signup', views.student_signup,name='student_signup'),
]