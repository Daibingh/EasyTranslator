# -*- coding: utf-8 -*-

import requests
import sys
import re
from bs4 import BeautifulSoup
# from multiprocessing import Process, Pool


# def langdetect(text):
#     url = 'http://fanyi.baidu.com/langdetect'
#     headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
#     rs = requests.post(url, headers=headers, data={'query': text[:min(len(text), 16)]})
#     if rs.status_code != 200:
#         print('请求错误代码: ', rs.status_code)
#         return None
#     if rs.json().get('error') != 0:
#         print('detect failed!')
#         return None
#     if rs.json().get('lan') == 'en':
#         return 1
#     else:
#         return 0

def langdetect(text):
    url = 'https://cn.bing.com/tdetect'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    rs = requests.post(url, headers=headers, data={'text': text})
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    if rs.text == 'zh-CHS':
        return 0
    else:
        return 1

def baiduTranslator(text, flg=0):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    data = {'from': 'zh', 'to': 'en', 'query': text}
    if flg != 0:
        data['from'] = 'en'
        data['to'] = 'zh'
    rs = requests.post('http://fanyi.baidu.com/basetrans', headers=headers, data=data)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    return rs.json()['trans'][0]['dst']


def youdaoTranslator(text, flg=0):
    url = 'http://m.youdao.com/translate'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    data = {
        'inputtext': text,
        'type': 'ZH_CN2EN'
    }
    if flg != 0:
        data['type'] = 'EN2ZH_CN'
    rs = requests.post(url, headers=headers, data=data)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    patern = re.compile(r'<ul id="translateResult">.*?<li>(.*?)</li>.*?</ul>', re.S)
    m = re.search(patern, rs.text)
    return m[1]


def jinshanTranslator(text, flg=0):
    url = 'http://fy.iciba.com/ajax.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    params = {'a': 'fy'}
    data = {'f': 'zh', 't': 'en', 'w': text}
    if flg != 0:
        data['f'] = 'en'
        data['t'] = 'zh'
        if text[-1] != '.':
            data['w'] = text + '.'
    rs = requests.post(url, params=params, headers=headers, data=data)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    return rs.json().get('content').get('out')


def bingTranslator(text, flg=0):
    url = 'https://cn.bing.com/ttranslate'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    data = {
        'text': text,
        'from': 'zh-CHS',
        'to': 'en'
    }
    if flg != 0:
        data['from'] = 'en'
        data['to'] = 'zh-CHS'
    rs = requests.post(url, headers=headers, data=data)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    return rs.json().get('translationResponse')


def cnkiTranslator(text, flg=0):
    url = 'http://dict.cnki.net/dict_result.aspx'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    params = {'searchword': text}
    rs = requests.get(url, params=params, headers=headers)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    # # print(rs.text)
    # e = etree.HTML(rs.text)
    # tables = e.xpath('//*[@id="lblresult"]/table[1]/tr/td[1]/table')
    # parseTable(tables)
    html = rs.text.replace('\r\n', '')
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.select('table.main-table')
    # print(len(e))
    # print(e[0].text)
    if len(tables) == 0:
        print('没有查找到翻译结果！')
        return None
    result = []
    for table in tables:
        if table.img is not None and table.img.attrs['src'] == 'images/02.gif':
            d1 = dict()
            for t in table.select('font.text9'):
                l = []
                next_tr = t.parent.parent.next_sibling
                tts = next_tr.findAll('font', {'class': 'text6'})
                for tt in tts:
                    l.append(tt.text)
                d1[t.text] = l[:min(4, len(l))]
            # print(d1)
            result.append(d1)
        elif table.img is not None and table.img.attrs['src'] == 'images/word.jpg':
            t2s = table.findAll('table', {'id': re.compile(r'showjd_\d')})
            d2 = dict()
            for t2 in t2s:
                l = []
                text_zhs = t2.select('td.text11Green')
                for text_zh in text_zhs:
                    l.append(text_zh.parent.previous_sibling.text.strip())
                    l.append(text_zh.text.strip())
                key = t2.previous_sibling.select('a[href^="javascript:showjdsw"]')[0].text
                d2[key] = l[:min(4, len(l))]
            # print(d2)
            result.append(d2)
        if len(result) == 2:
            break
    return result

def googleTraslator(text, flg=0):
    url = 'https://translate.google.cn/m'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    params = {
        'hl': 'zh-CN',
        'sl': 'zh-CN',
        'tl': 'en',
        'ie': 'UTF-8',
        'q': text
    }
    if flg != 0:
        params['sl'] = 'en'
        params['tl'] = 'zh-CN'
    rs = requests.get(url, headers=headers, params=params)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    soup = BeautifulSoup(rs.text.replace('\r\n', ''), 'lxml')
    return soup.find('div', {'dir': 'ltr', 'class': 't0'}).text


def printresult(fun, text):
    print(fun(text))

if __name__ == '__main__':
    # p = Pool()
    # p.apply_async(printresult, args=(baiduTranslator, text))
    # p.apply_async(printresult, args=(googleTraslator, text))
    # p.apply_async(printresult, args=(bingTranslator, text))
    # p.apply_async(printresult, args=(jinshanTranslator, text))
    # p.apply_async(printresult, args=(youdaoTranslator, text))
    # p.apply_async(printresult, args=(cnkiTranslator, text3))
    # p.close()
    # p.join()
    # print('--------END--------')

    text = '百度翻译是百度发布的在线翻译服务，依托互联网数据资源和自然语言处理技术优势，致力于帮助用户跨越语言鸿沟，方便快捷地获取信息和服务。'
    text2 = 'In this paper, a complete set of road traffic flow measurement system based on modular algorithm is established for traffic flow analysis of road vehicles. The whole road traffic flow measurement system consists of three parts: image preprocessing module, vehicle detection module and traffic flow statistics module'
    text3 = '人工智能'
    text4 = 'artificial'
    # print(langdetect(text2))
    # print(jinshanTranslator(text4, 1))
    print(baiduTranslator(text))
    # print(youdaoTranslator(text2, 1))
    # print(bingTranslator(text))
    # print(googleTraslator(text2, 1))
    # print(cnkiTranslator(text3))

