import requests
from users import models

# 请求微信 openid
def getOpenid(appid, secret, code):
    openid = requests.get(r'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code')
    return openid.json()

# 获取学号密码
def getUP(openid):
    up = models.UserInfo.objects.filter(wxid=openid).values_list('username', 'password', 'autologin')
    return list(up)


# 添加学生信息
def addUser(userinfo, openid):
    un = userinfo['xh'] # 学号
    pw = userinfo['mm'] # 密码
    nm = userinfo['xm'] # 姓名
    cn = userinfo['bm'] # 班名
    sex = userinfo['xb']    # 性别
    col = userinfo['xsm']   # 学院名
    cam = userinfo['xqm']   # 校区名
    pro = userinfo['zym']   # 专业名

    result = models.UserInfo.objects.create(username=un, password=pw, studentname=nm, wxid=openid, autologin=1, sex=sex, classname=cn, college=col, campus=cam, professional=pro )
    return result

# 修改四六级考号
def setCET(username, cetnum):
    result = models.UserInfo.objects.filter(username=username).update(CET_number=cetnum)
    return result

# 设置是否自动登录
def setAutologin(username, openid):
    sr = models.UserInfo.objects.filter(username=username).values_list('autologin')
    print()
    autoflag = (list(sr)[0][0] + 1) % 2
    result = models.UserInfo.objects.filter(username=username).update(autologin=autoflag, wxid=openid)
    return result

# 获取用户信息
def getUserinfo(username):
    result = models.UserInfo.objects.filter(username=username).all()
    return result
