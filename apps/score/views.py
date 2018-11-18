# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
import json
from package.jiaowu.jiaowu import jiaowuSpider
from package.imgRec.verificationCode import getVCode

# Create your views here.
'''
    TODO: 查成绩
'''
jiaowuSpider = jiaowuSpider()


# 验证码图片
def _VCodePicture():
    '''
    获取验证码图片，返回图片的二进制数据
    :return:
    '''
    while True:
        vcode = jiaowuSpider.getVerificationCodePicture()
        if not type(vcode) == dict:
            return vcode
            break


# 登录
def login(req):
    '''
    获取用户输入的用户名密码，调用验证码识别获取验证码登录
    :param req:
    :return:
    '''
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        while True:
            # 获取验证码图片
            vcodedata = _VCodePicture()
            # 识别验证码
            vcode = getVCode(vcodedata)
            if len(vcode) != 4:
                continue
            # 登录
            loginResult = jiaowuSpider.login(username, password, vcode)
            if not loginResult['code'] == 1301:
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