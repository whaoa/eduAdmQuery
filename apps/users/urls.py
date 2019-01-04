from django.urls import path
from users import views

urlpatterns = [
    path(r'media', views.getImageUrl, name="getImageUrl"), # 获取图片
    path(r'getUP', views.getUP), #获取学号密码
    path(r'userinfo', views.userInfo), # 用户信息
    path(r'autologin', views.setAutologin), # 设置自动登录
    path(r'cetNum', views.CETNum), # 四六级考号
]
