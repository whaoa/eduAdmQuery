import copy
from django.http import HttpResponse

from package.db import db

'''
    TODO: 获取课表信息
'''

def getTimetable(clas, week=-1, weekday=-1, timeblock=-1):
    '''
    :param clas: 班级
    :param week: 第几周 1-19
    :param weekday: 星期 0-6
    :param timeblock: 时间段
    :return: list
    '''

    week, weekday, timeblock = int(week), int(weekday), int(timeblock)
    # 获取课表
    cls = list(db.timetables.find({'classname': clas}))

    if len(cls) == 0:
        return []
    list_cls = cls[0]['timetable']
    # 全部课表
    if week == -1 and weekday == -1 and timeblock == -1:
        return list_cls

    # 今日课表
    if not weekday == -1:
        todayTimetable = []
        for a in list_cls:
            if week in a[weekday][0]['weeks']:
                todayTimetable.append(a[weekday])

        # 某时间块课表
        if not timeblock == -1:
            todayTimetable = list_cls[timeblock][weekday]
        return todayTimetable
    # 本周课表
    elif not week == -1:
        weekTimetable = []
        for a in list_cls:
            tmpTimeblock = []
            for b in a:
                if b[0]['name'] == None:
                    tmpTimeblock.append([])
                elif week in b[0]['weeks']:
                    tmpTimeblock.append(b)
                elif not week in b[0]['weeks']:
                    tmpTimeblock.append([])
            weekTimetable.append(copy.deepcopy(tmpTimeblock))
        return weekTimetable

