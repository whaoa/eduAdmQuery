from django.shortcuts import render
from django.http import HttpResponse
import json

from package._date.schoolWeek import getAppointDateInfo

# Create your views here.

def getAppointDate(req):
    if req.method == 'GET':
        year = int(req.GET.get('year','')) if not req.GET.get('year','') == '' else None
        month = int(req.GET.get('month','')) if not req.GET.get('month','') == '' else None
        day = int(req.GET.get('day','')) if not req.GET.get('day','') == '' else None
        week = int(req.GET.get('week','')) if not req.GET.get('week','') == '' else None

        dateInfo = getAppointDateInfo(year, month, day, week)
        r = {'status': 'success', 'code': 4601, 'body': dateInfo}
        return HttpResponse(json.dumps(r, ensure_ascii=False))
    else:
        r = {'status': 'error', 'code': 1502, 'body': '请求方法错误，应当是 GET。'}
        return HttpResponse(json.dumps(r, ensure_ascii=False))