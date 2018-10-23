from django.shortcuts import render
from django.http import HttpResponse
import json
from package.jiaowu.timetable import getTimetable


# Create your views here.

def timetable(req):
    if req.method == 'GET':
        clas = req.GET.get('clas', -1)
        week = req.GET.get('week', -1)
        weekday = req.GET.get('weekday', -1)
        timeblock = req.GET.get('timeblock', -1)
        if not clas == -1:
            tt = getTimetable(clas, week, weekday, timeblock)
            r = {'status': 'success', 'code': 3601, 'body': tt}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
        else:
            r = {'status': 'success', 'code': 3602, 'body':'请输入班级参数'}
            return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法应该是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))
