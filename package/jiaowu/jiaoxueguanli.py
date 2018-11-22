
import requests
import random
from urllib import parse

'''
    @TODO:查排名
    @TODO:查补考
'''


class jiaowuSpider():

    def login(self, u, p):
        '''
            TODO:登录
        '''
        logindata = {
            'u': u,
            'p': p,
            'r': 'on'
        }
        loginResult = requests.post('http://202.207.247.60/Hander/LoginAjax.ashx', data=logindata)
        if loginResult.json()['Code'] == 1:
            # 登录成功
            cookie = requests.utils.dict_from_cookiejar(loginResult.cookies)
            return cookie
        else:
            return 'error'

    def getRanking(self,username,  cookie):
        '''
            TODO:查排名
        '''
        data = {
            'limit': '40',
            'offset': '0',
            'order': 'asc',
            'sort': 'jqzypm,xh',
            'do': 'xsgrcj',
            'xh': username
        }
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        rankResult = requests.post('http://202.207.247.60/Hander/Cj/CjAjax.ashx?rnd%20=%20' + str(random.random()), data=data, cookies=ck_jar)
        if rankResult.status_code == 200:
            return rankResult.json()[0]
        else:
            return {}

    def getMakeupExam(self, username,  cookie):
        '''
            TODO:查补考
        '''
        data = {
            'limit': '30',
            'offset': '0',
            'order': 'asc',
            'sort': 'zc,xq,ksjc',
            'do': 'getbkkssjbyxh',
            'zxjxjhh': '2018-2019-1-1',
            'xh' : username
        }
        # 将cookie转为cookiejar对象
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        makeupExamResult = requests.post('http://202.207.247.60/Hander/Ks/Bkks/KsbkAjax.ashx?rnd=' + str(random.random()), data=data, cookies=ck_jar)
        if makeupExamResult.status_code == 200:
            return makeupExamResult.json()['rows']
        else:
            return []

    def getStudentInfo(self,username,  cookie):
        '''
        TODO: 获取学生基本信息
        :return:
        '''

        data = {
            'limit' : '40',
            'offset' : '0',
            'order' : 'desc',
            'sort' : 'xh',
            'do' : 'getlist',
            'xh' : username,
        }
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        studentInfo = requests.post('http://202.207.247.60/Hander/Students/StudentsAjax.ashx?rnd=' + str(random.random()), data=data, cookies=ck_jar)
        if studentInfo.status_code == 200:
            return studentInfo.json()['rows'][0]
        else:
            return {}

