from django.urls import path
from timetable import views

urlpatterns = [
    path(r'timetable', views.timetable, name="getTimetable"), # 获取课表

]
