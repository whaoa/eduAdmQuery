import requests
data = {
    'u': 2017007700,
    'p': 292530
}
res = requests.post('http://202.207.247.60/Hander/LoginAjax.ashx',data=data)
cookie = res.cookies
ck_dict = requests.utils.dict_from_cookiejar(cookie)
print(ck_dict)
ck_jar = requests.utils.cookiejar_from_dict(ck_dict)
data = {
    'limit':40,
    'offset':0,
    'order':'asc',
    'sort':'jqzypm%2Cxh',
    'do':'xsgrcj',
    'xh':2017007700,
}
res2 = requests.post('http://202.207.247.60/Hander/Cj/CjAjax.ashx?rnd%20=%200.6621790734277038', data = data, cookies=ck_jar)
print(res2.text)