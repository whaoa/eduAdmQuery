
import requests
import random

'''
    @TODO:查排名
    @TODO:查补考
'''


class jiaowuSpider():
    _rs = requests.Session()

    def login(self, u, p):
        '''
            TODO:登录
        '''
        self.u = u
        self.p = p
        logindata = {
            'u': u,
            'p': p,
            'r': 'on'
        }
        loginResult = self._rs.post('http://202.207.247.60/Hander/LoginAjax.ashx', data=logindata)
        if loginResult.json()['Code'] == 1:
            # 登录成功
            return 1
        else:
            return 2

    def getRanking(self):
        '''
            TODO:查排名
        '''
        data = {
            'limit': '40',
            'offset': '0',
            'order': 'asc',
            'sort': 'jqzypm,xh',
            'do': 'xsgrcj',
            'xh': self.u
        }
        rankResult = self._rs.post('http://202.207.247.60/Hander/Cj/CjAjax.ashx?rnd%20=%20' + str(random.random()), data=data)
        if rankResult.status_code == 200:
            return rankResult.json()[0]
        else:
            return {}

    def getMakeupExam(self):
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
            'xh' : self.u,
        }
        makeupExamResult = self._rs.post('http://202.207.247.60/Hander/Ks/Bkks/KsbkAjax.ashx?rnd=' + str(random.random()), data=data)
        if makeupExamResult.status_code == 200:
            return makeupExamResult.json()['rows']
        else:
            return []

    def getStudentInfo(self):
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
            'xh' : self.u,
        }
        studentInfo = self._rs.post('http://202.207.247.60/Hander/Students/StudentsAjax.ashx?rnd=' + str(random.random()), data=data)
        if studentInfo.status_code == 200:
            return studentInfo.json()['rows'][0]
        else:
            return {}

