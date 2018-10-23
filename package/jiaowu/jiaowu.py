
import requests
import random
from bs4 import BeautifulSoup


'''
    TODO:查成绩
    TODO:查不及格成绩
'''


class jiaowuSpider:
    _rs = requests.Session()
    def getVerificationCodePicture(self):
        '''
         TODO:获取验证码图片
        '''
        try:
            getYzmPicture = self._rs.get('http://202.207.247.44:8089/validateCodeAction.do?random=' + str(random.random()))
        except requests.exceptions:
            return {'status':'error', 'code':1201, 'body':'查成绩获取验证码请求失败'}
        return getYzmPicture.content


    def login(self, username, password, yzm):
        '''
            TODO:登录
        '''
        data = {
            'zjh': username,
            'mm': password,
            'v_yzm': yzm
        }
        try:
            loginResult = self._rs.post('http://202.207.247.44:8089/loginAction.do', data=data)
        except requests.exceptions:
            return {'status':'error', 'code':1202, 'body':'查成绩教务处登录请求失败'}
        if loginResult.status_code == 200:
            if '验证码错误' in loginResult.text:
                return {'status':'fail', 'code':1301, 'body':'验证码错误'}
            elif '密码不正确' in loginResult.text:
                return {'status': 'fail', 'code': 1302, 'body': '密码不正确'}
            elif '证件号不存在'in loginResult.text:
                return {'status': 'fail', 'code': 1303, 'body': '证件号不存在'}
            else:
                return {'status': 'success', 'code': 1401, 'body': '查成绩教务处登录成功'}
        else:
            return {'status':'error', 'code':1203, 'body':'查成绩教务处登录请求失败'}

    def getScore(self):
        '''
            TODO:查成绩
            :return: semesters{[],[]}
        '''
        try:
            scoreResult = self._rs.get('http://202.207.247.44:8089/gradeLnAllAction.do?type=ln&oper=qbinfo')
        except requests.exceptions:
            print('ERROR：查成绩请求错误！')
            return
        soup = BeautifulSoup(scoreResult.text, 'lxml')
        lab_a = soup.find_all('a')
        semesters = {}
        for a in lab_a:
            semester = a['name']
            if not semester in list(semesters.keys()):
                semesters[semester] = []
            titleTop2 = a.find_next_sibling('table',class_='titleTop2')
            odds = titleTop2.find_all(class_='odd')
            for odd in odds:
                _info = odd.getText().split()
                info = _info[0:3]+_info[-3:]
                semesters[semester].append(info)
        return semesters

    def getFailScore(self):
        '''
            TODO:查不及格成绩
            :return: clss{[[]],[[]]}
        '''
        try:
            scoreResult = self._rs.get('http://202.207.247.44:8089/gradeLnAllAction.do?type=ln&oper=bjg')
        except requests.exceptions:
            return '错误'
        soup = BeautifulSoup(scoreResult.text, 'lxml')
        body = soup.find(class_='table_k').find('td')
        lab_a = body.find_all('table',id='tblHead')
        clss = {}
        for a in lab_a:
            cl = a.find('b').text.strip()
            if not cl in list(clss.keys()):
                clss[cl] = []
            titleTop2 = a.find_next_sibling('table',class_='titleTop2')
            odds = titleTop2.find_all(class_='odd')
            for odd in odds:
                _info = odd.getText().split()
                info = _info[0:3]+_info[-4:]
                clss[cl].append(info)
        return clss

