
import requests
import random
import json
from bs4 import BeautifulSoup


'''
    TODO:查成绩
    TODO:查不及格成绩
'''


class jiaowuSpider:
    def getVerificationCodePicture(self):
        '''
         TODO:获取验证码图片
        '''
        try:
            getYzmPicture = requests.get('http://202.207.247.44:8089/validateCodeAction.do?random=' + str(random.random()))
        except requests.exceptions:
            return {'status':'error', 'code':1201, 'body':'查成绩获取验证码请求失败'}
        cookie = requests.utils.dict_from_cookiejar(getYzmPicture.cookies)
        return getYzmPicture.content, cookie


    def login(self, username, password, yzm, cookie):
        '''
            TODO:登录
        '''
        data = {
            'zjh': username,
            'mm': password,
            'v_yzm': yzm
        }
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        try:
            loginResult = requests.post('http://202.207.247.44:8089/loginAction.do', data=data, cookies=ck_jar)
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
                return {'status': 'success', 'code': 1401, 'body': cookie}
        else:
            return {'status':'error', 'code':1203, 'body':'查成绩教务处登录请求失败'}

    def getScore(self, cookie):
        '''
            TODO:查成绩
            :return: semesters{[],[]}
        '''
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        try:
            scoreResult = requests.get('http://202.207.247.44:8089/gradeLnAllAction.do?type=ln&oper=qbinfo', cookies=ck_jar)
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

    def getFailScore(self, cookie):
        '''
            TODO:查不及格成绩
            :return: clss{[[]],[[]]}
        '''
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        try:
            scoreResult = requests.get('http://202.207.247.44:8089/gradeLnAllAction.do?type=ln&oper=bjg', cookies=ck_jar)
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

    def evaluate(self, cookie):
        ck_jar = requests.utils.cookiejar_from_dict(cookie)
        try:
            listpagehtml = requests.get(r'http://202.207.247.44:8089/jxpgXsAction.do?oper=listWj', cookies=ck_jar)
        except requests.exceptions as e:
            print(e)
            return '错误'
        soup = BeautifulSoup(listpagehtml.text, 'lxml')
        imglist = soup.find_all('img', title='评估')
        cklist = soup.find_all('img', title='查看')

        if len(imglist) == 0 and len(cklist) == 0:
            return '评教已结束'
        elif  len(imglist) == 0 and len(cklist) != 0:
            return '已评教'

        result = True
        for i in range(len(imglist)):
            info = str(imglist[i]).split('" ')[2][6:].split('#@')
            info = info[0:2] + info[-1:]
            data = {
                'wjbm': info[0],
                'bpr': info[1],
                'pgnr': info[2],
                '0000000136': '25_0.95',
                '0000000137': '25_0.95',
                '0000000138': '30_0.95',
                '0000000139': '20_0.95',
                'zgpj': '很棒'
            }
            postResult = requests.post('http://202.207.247.44:8089/jxpgXsAction.do?oper=wjpg', data=data,cookies=ck_jar)
            if '失败' in postResult:
                result = False
        return result