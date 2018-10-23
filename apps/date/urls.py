from django.urls import path
from date import views

urlpatterns = [
    path(r'appointDate', views.getAppointDate, name="getAppointDate"),
]
