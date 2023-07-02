from django.urls import path
from Student import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('student_view', views.student_view),
    path('student_login', LoginView.as_view(template_name='student/student_login.html'),name='student_login'),
    path('student_signup', views.student_signup,name='student_signup'),


    path('student-dashboard', views.student_dashboard,name='student-dashboard'),
    path('student-exam', views.student_exam,name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam,name='take-exam'),
    path('start-exam/<int:pk>', views.start_exam,name='start-exam'),


    path('calculate-marks', views.calculate_marks,name='calculate-marks'),
    path('view-result', views.view_result,name='view-result'),
    path('check-marks/<int:pk>', views.check_marks,name='check-marks'),
    path('student-marks', views.student_marks,name='student-marks'),

]