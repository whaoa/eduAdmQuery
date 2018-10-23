import re
import urllib.parse
import string
import pymongo
import copy

'''
    TODO:下载课表并存到数据库
'''

# 链接数据库
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.TYUT


def getClassSchedule(self):
    '''
        TODO:查课表
    :return:
    '''
    # 访问课表的菜单栏页面，不请求这个页面直接请求课表会 500 错误。
    temp = self._rs.get('http://202.207.247.44:8089/bjkbcxAction.do?oper=bjkb_lb')
    data = {
        'bjxnxq': '2018-2019-1-1',
        'pageSize': '1100',
        'page': '1',
        'currentPage': '1',
        'bjzyh': '',
        'bjxsh': '',
        'nj': '',
        'bj': '',
        'pageNo': '',
    }
    classs = self._rs.post('http://202.207.247.44:8089/bjkbcxAction.do?oper=kbtjcx', data=data)
    r = re.compile(
        r'''<tr class="odd".*?>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?onclick="bjkb_xx\('([\s\S]*?)'\)[\s\S]*?</tr>''')
    classlist = r.findall(classs.text)
    classInfo = []
    # 获取所有班级课表链接
    for i in range(len(classlist)):
        info = {}
        info['number'] = classlist[i][0].strip()
        info['class1'] = classlist[i][1].strip()
        info['class2'] = classlist[i][2].strip()
        info['college'] = classlist[i][3].strip()
        info['major'] = classlist[i][4].strip()
        info['timetableUrl'] = classlist[i][5].strip()
        classInfo.append(info)
    # 保存到文件
    # with open('allClassInfo.json','w') as f:
    # f.write(json.dumps(classInfo).encode('utf-8').decode('unicode_escape'))
    t = 0
    for item in classInfo:
        # 妈的，这里要写 GBK 编码，搞一下午，卧槽。
        # 将获取道德课程表路由进行 url编码，并且跳过指定字符 safe 参数，指定编码为 gbk
        url = urllib.parse.quote(item['timetableUrl'], safe=string.printable, encoding="gbk")
        timetableHtml = self._rs.get('http://202.207.247.44:8089/' + url)
        # 获取课表信息
        rex = re.compile(r'<td width="12%" valign="top">([\s\S]*?)</td>')
        subjectInfo = rex.findall(timetableHtml.text)
        # 获取学期和班级
        cs = re.compile(r'学年学期:[\s\S]*?<td>([\s\S]*?\))[\s\S]*?班级名称:[\s\S]*?<td>([\s\S]*?\d{4})').findall(
            timetableHtml.text)[0]
        classname = cs[1]
        semester = cs[0]
        timetable = {
            'semester': semester,
            'classname': classname,
            'timetable': [],
        }

        # 获取课表详细信息
        flag = 0
        daytable = []
        for sub in subjectInfo:
            flag += 1
            subject = sub.replace('&nbsp;', '').replace('<br>', '').strip().replace('\t', '').replace(' ', '')
            info = re.findall(r'(.*)?\((.*)?校区(.*?),(.*?),(.*?),(.*?)周上', subject)
            info = list(info) if info else [(None, None, None, None, None, None)]

            # 块
            block = []
            # 同一时间段的不同周有不同课程
            for item in info:
                # 获取单节课详细信息
                weeks = []
                if not item[5] == None:
                    if ',' in item[5]:
                        for a in item[5].split(','):
                            if '-' in a:
                                weeks += list(range(int(a[0: a.index('-')]), int(a[a.index('-') + 1:]) + 1))
                            else:
                                weeks.append(int(a))
                    else:
                        if '-' in item[5]:
                            weeks += list(
                                range(int(item[5][0: item[5].index('-')]), int(item[5][item[5].index('-') + 1:]) + 1))
                        else:
                            weeks.append(int(item[5]))
                else:
                    weeks = None
                clas = {
                    'name': item[0],
                    'campus': item[1],
                    'floor': item[2],
                    'classroom': item[3],
                    'teacher': item[4],
                    'weeks': weeks
                }
                block.append(clas)

            daytable.append(copy.deepcopy(block))
            block.clear()
            # 换时间段
            if flag % 7 == 0:
                timetable['timetable'].append(copy.deepcopy(daytable))
                daytable.clear()

        # 写入文件保存
        # with open('timetable.json', 'a+', encoding='utf-8') as f:
        #     f.write(json.dumps(timetable).encode('utf-8').decode('unicode-escape'))
        #     f.write(',')
        #     f.write('\n')
        # 存到数据库
        result = db.timetables.insert_one(timetable)
        t += 1
        print(t, end=': ')
        print(result)

