
from package.db import db
import datetime

yearNow = datetime.datetime.now().year
monthNow = datetime.datetime.now().month
dayNow = datetime.datetime.now().day


def getAppointDateInfo(year=yearNow, month=monthNow, day=dayNow, week=None):
    '''
    TODO: 获取指定日期的日期信息，可指定年月日或周的其中之一，周优先。默认当天的信息。
    :param year: 指定年
    :param month: 指定月
    :param day: 指定天
    :param week: 指定第几周，优先
    :return: 年月日[]， 周 {'s1':[], 's2':[]} '_id'字段表示当天在该学年第几天
    '''
    year = yearNow if year == None else year
    month = monthNow if month == None else month
    day = dayNow if day == None else day

    if not week == None:
        week = int(week)
        dateInfo = list(db.schoolWeek.find({'schoolWeek':week}))
        if len(dateInfo) > 7:
            return {'s1': dateInfo[0:7],'s2':dateInfo[7:]}
        else:
            return {'s1': dateInfo}
    else:
        dateInfo = list(db.schoolWeek.find({'year':year,'month':month, 'day':day}))
        if len(dateInfo) == 0:
            return 'Date error! 不在时间范围内。'
        else:
            return dateInfo[0]
