from django.db import models

# Create your models here.
from django.db import models
import datetime


class UserInfo(models.Model):
    username = models.CharField('学号', max_length=16, primary_key=True, unique=True)
    password = models.CharField('密码', max_length=20, default='')
    studentname = models.CharField('姓名', max_length=10, default='')
    wxid = models.CharField('微信openid', max_length=50, default='')
    autologin = models.IntegerField('是否自动登录',default=0)
    sex = models.CharField('性别', max_length=5, default='')
    CET_number = models.CharField('四六级考号', max_length=20, default='')
    classname = models.CharField('班名', max_length=10, default='')
    professional = models.CharField('专业', max_length=30, default='')
    college = models.CharField('学院', max_length=20, default='')
    campus = models.CharField('校区', max_length=10, default='')
    create_time = models.DateTimeField('创建时间', default=datetime.datetime.now)