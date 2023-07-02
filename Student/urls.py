from django.urls import path
from Student import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('student_view', views.student_view),
    path('student_login', LoginView.as_view(template_name='student/student_login.html'),name='student_login'),
    path('student_signup', views.student_signup,name='student_signup'),


    path('student-dashboard', views.student_dashboard,name='student-dashboard'),


    path('student-exam', views.student_exam,name='student-exam'),
    path('student-exam-take/<int:pk>', views.exam_take,name='student-exam-take'),
    path('student-exam-start/<int:pk>', views.exam_start,name='student-exam-start'),
    path('student-exam-marks', views.exam_marks,name='student-exam-marks'),
    path('student-exam-result', views.exam_result,name='student-exam-result'),


    path('student-marks', views.student_marks,name='student-marks'),
    path('student-marks-see/<int:pk>', views.marks_see,name='student-marks-see'),
]