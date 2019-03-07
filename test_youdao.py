# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time

# reload(sys)
# sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '5eb6fc4657fa8bed'
APP_SECRET = 'ZsTtD0FHq9HwLwX7KBnGu5U9k3ZiJI1l'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect():
    q = "Process finished with exit code 0"

    data = {}
    data['from'] = 'EN'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    print(response.text)


if __name__ == '__main__':
    connect()
