from django.urls import path
from rank import views

urlpatterns = [
    path(r'login', views.login, name="loginRank"),
    path(r'rank', views.rank, name="getRanking"),
    path(r'makeupexam', views.makeUpExam, name="getMakeUpExam"),
    path(r'studentInfo', views.studentInfo, name='getStudentInfo')
]
