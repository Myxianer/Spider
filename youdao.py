import requests
import time
import json
import random
import hashlib


def get_ts():
    # 获取时间戳
    ts = int(time.time()*1000)
    return ts

def get_bv():
    # 生成bv
    appVersion = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    m = hashlib.md5()
    m.update(appVersion.encode('utf-8'))
    bv = m.hexdigest()
    return bv

def get_salt(ts):
    # 生成salt
    num = int(random.random()*10)
    salt = str(ts) + str(num)
    return salt

def get_sign(salt):
    # 生成sign
    a = 'fanyideskweb'
    b = fanyi
    c = salt
    d = '97_3(jkMYg@T[KZQmqjTK'

    str_data = a + b + c + d

    # md5加密
    m = hashlib.md5()
    m.update(str_data.encode('utf-8'))
    sign = m.hexdigest()

    return sign

def get_from_data():
    global fanyi
    ts = get_ts()
    salt = get_salt(ts)

    from_data = {
        "i": fanyi,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": str(salt),
        "sign": get_sign(salt),
        "ts": str(ts),
        "bv": get_bv(),
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }

    return from_data

def main():
    global fanyi
    print("请输入你想翻译的中文：")
    fanyi = str(input())
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer':'http://fanyi.youdao.com/',
        'Cookie':'OUTFOX_SEARCH_USER_ID=762609870@10.168.8.63; JSESSIONID=aaa2aaM8zIqafcMZ-GqVw; OUTFOX_SEARCH_USER_ID_NCOO=1685517028.593034; ___rl__test__cookies=1562597449226'
    }

    response = requests.post(url, data=get_from_data(), headers=headers)
    dict_result = json.loads(response.content)
    print("翻译结果：", dict_result['translateResult'][0][0]['tgt'])


if __name__ == '__main__':
    main()
