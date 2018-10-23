# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
import json
from package.jiaowu.jiaowu import jiaowuSpider

# Create your views here.
'''
    TODO: 查成绩
'''
jiaowuSpider = jiaowuSpider()


# 验证码图片
def verificationCodePicture(req):
    if req.method == 'GET':
        vcp = jiaowuSpider.getVerificationCodePicture()
        if not type(vcp) == dict:
            return HttpResponse(vcp,content_type="image/jpg")
        else:
            return HttpResponse(vcp)
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))


# 登录
def login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        verificationCode = req.POST.get('verificationCode')
        loginResult = jiaowuSpider.login(username, password, verificationCode)
        return HttpResponse(json.dumps(loginResult, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code':1501, 'body': '请求方法错误，应当是 POST。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))


# 查询成绩
def score(req):
    if req.method == 'GET':
        sc = jiaowuSpider.getScore()
        r = {'status':'success', 'code':1601, 'body':sc}
        return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code':1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))


# 查不及格成绩
def failScore(req):
    if req.method == 'GET':
        fsc = jiaowuSpider.getFailScore()
        r = {'status': 'success', 'code': 1601, 'body': fsc}
        return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code':1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))