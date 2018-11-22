from django.shortcuts import render
from django.http import HttpResponse
import json
from urllib import parse
from package.jiaowu.jiaoxueguanli import jiaowuSpider

jiaowuSpider = jiaowuSpider()

# Create your views here.

'''
    TODO: 查排名、补考      
'''

# 登录
def login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        # 返回的是 cookie dict
        loginResult = jiaowuSpider.login(username, password)

        if loginResult != 'error':
            r = {'status':'success', 'code':2401, 'body':loginResult}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            r = {'status':'fail','code':2301, 'body':'登录失败，账号或密码错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code':1501, 'body': '请求方法错误，应当是 POST。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))

# 获取排名
def rank(req):
    if req.method == 'GET':
        # 获取 cookie
        cookie = req.GET.get('cookie')
        username = req.GET.get('username')
        # url解码
        cookie = json.loads(parse.unquote(cookie))
        if cookie == '':
            return {'status':'fail', 'code':'0', 'body':'login error'}
        # 请求
        rankResult = jiaowuSpider.getRanking(username, cookie)
        if rankResult:
            r = {'status':'success', 'code':'2601', 'body':rankResult}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            r = {'status':'error', 'code':2201, 'body':'请求教务处失败'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))

# 查补考
def makeUpExam(req):
    if req.method == 'GET':
        # 获取cookie
        cookie = req.GET.get('cookie')
        username = req.GET.get('username')
        # url解码
        cookie = json.loads(parse.unquote(cookie))
        # 请求
        makeUpExamResult = jiaowuSpider.getMakeupExam(username, cookie)
        if makeUpExamResult:
            r = {'status':'success', 'code':'2601', 'body':makeUpExamResult}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            r = {'status':'error', 'code':2202, 'body':'请求教务处失败'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))

# 获取学生信息
def studentInfo(req):
    if req.method == 'GET':
        # 获取cookie
        cookie = req.GET.get('cookie')
        username = req.GET.get('username')
        # url解码
        cookie = json.loads(parse.unquote(cookie))
        # 请求
        info = jiaowuSpider.getStudentInfo(username, cookie)
        if info:
            r = {'status':'success', 'code':'2601', 'body':info}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            r = {'status':'error', 'code':2202, 'body':'请求教务处失败'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))