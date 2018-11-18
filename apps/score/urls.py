from django.urls import path
from score import views

urlpatterns = [
    path(r'login', views.login, name="loginScore"),
    path(r'score', views.score, name="getScore"),
    path(r'failScore', views.failScore, name="getFailScore"),

]
