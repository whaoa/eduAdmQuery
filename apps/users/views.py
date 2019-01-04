from django.shortcuts import render
from django.http import HttpResponse
import json
import os
import package.userfunc.userfunc as uf

# Create your views here.


appid = 'wx135d16bff5b5ceb7'
secret = 'aa2cb6faa97aaf8d7ae3009ab82f1fb9'
# 获取图片的 url
def getImageUrl(req):
    if req.method == 'GET':
        router = req.GET.get('router')
        fileList = os.listdir(r'media/' + router + '/')
        urlList = ['https://www.twohac.com:8000/media/'+ router + '/' + f for f in fileList]
        r = {'status': 'success', 'msg':'请求文件成功', 'body': urlList}
        return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1501, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))

# 根据微信查询学号和密码
def getUP(req):
    # GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    if req.method == 'GET':
        code = req.GET.get('code', '')
        if code == '':
            r = {'status': 'fail', 'body': 'code 参数错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            wxid = uf.getOpenid(appid, secret, code)
            openid = wxid['openid']
            up = uf.getUP(openid)
            up = up[0] if len(up) != 0 else up
            if up == [] or up[2] == 0:
                up = []
            r = {'status': 'success', 'body': up}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1501, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))


# 学生信息
def userInfo(req):
    if req.method == 'POST':
        userinfo = req.POST.get('userinfo', '')
        code = req.POST.get('code', '')
        if code == '' or userinfo == '':
            r = {'status': 'fail', 'body': '参数错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            userinfo = json.loads(userinfo)
            appid = 'wx135d16bff5b5ceb7'
            secret = 'aa2cb6faa97aaf8d7ae3009ab82f1fb9'
            # 获取 openid
            wxid = uf.getOpenid(appid, secret, code)
            openid = wxid['openid']
            # 判断用户是否已存在
            haveUser = uf.getUserinfo(userinfo['xh'])
            if len(haveUser) != 0:
                r = {'status': 'success', 'body': '用户已存在'}
            else:
                sr = uf.addUser(userinfo, openid)
                r = {'status': 'success', 'body': '添加成功'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        # 获取数据库中用户信息，（只有自动登录flag）
        username = req.GET.get('username', '')
        if username == '':
            r = {'status': 'error',  'body': '参数错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            result = uf.getUserinfo(username)
            if len(result) == 0:
                r = {'status': 'success', 'body': ''}
                return HttpResponse(json.dumps(r, ensure_ascii=False))
            autoflag = result[0].autologin
            r = {'status': 'success', 'body': autoflag}
            return HttpResponse(json.dumps(r, ensure_ascii=False))

# 四六级考号
def CETNum(req):
    if req.method == 'POST':
        cetnum = req.POST.get('cetnum', '')
        username = req.POST.get('username', '')
        if cetnum == '' or username == '':
            r = {'status': 'fail', 'body': '参数错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            sr = uf.setCET(username, cetnum)
            r = {'status': 'success', 'body': 'OK'} if sr == 1 else {'status': 'fail', 'body': '错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        username = req.GET.get('username','')
        if username == '':
            r = {'status': 'fail', 'body': '请求参数错误'}
        else:
            result = uf.getUserinfo(username)
            if len(result) == 0:
                r = {'status':'success', 'body': ''}
                return HttpResponse(json.dumps(r, ensure_ascii=False))
            cetnum = result[0].CET_number
            r = {'status':'success', 'body': cetnum}
            return HttpResponse(json.dumps(r, ensure_ascii=False))

# 设置是否自动登录
def setAutologin(req):
    if req.method == 'POST':
        username = req.POST.get('username', '')
        code = req.POST.get('code', '')
        if username == '' or code == '':
            r = {'status': 'fail', 'body': '参数错误'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            wxid = uf.getOpenid(appid, secret, code)
            openid = wxid['openid']
            sr = uf.setAutologin(username, openid)
            r = {'status': 'success', 'body': '设置成功'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法错误，应当是 POST。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))

