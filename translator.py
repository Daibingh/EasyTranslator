# -*- coding: utf-8 -*-

import requests
import sys
import re
from bs4 import BeautifulSoup
import random
from hashlib import md5
from urllib.parse import quote
from config import appid, secretKey


timeout = 2

def langdetect(text):
    url = 'https://cn.bing.com/tdetect'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    rs = requests.post(url, headers=headers, data={'text': text}, timeout=timeout)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    if rs.text == 'zh-CHS':
        return 0
    else:
        return 1

def baiduTranslator(text, flg=0):
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36'}
    appid = 20180906000203440
    secretKey = 'hi6HmTHso5erk8RQoyUD'
    # appid = 00000
    # secretKey = 'xxxxxx'
    salt =  random.randint(32768, 65536)
    t = str(appid) + text + str(salt) + secretKey
    sign = md5(t.encode('utf-8')).hexdigest()
    data = {
        'from': 'zh',
        'to': 'en',
        'q': text,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    if flg != 0:
        data['from'] = 'en'
        data['to'] = 'zh'
    rs = requests.post(url, headers=headers, data=data, timeout=timeout)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    return rs.json()['trans_result'][0]['dst']


def youdaoTranslator(text, flg=0):

    url = 'http://m.youdao.com/translate'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Mobile Safari/537.36'}
    data = {
        'inputtext': text,
        'type': 'AUTO'
    }
    rs = requests.post(url, headers=headers, data=data)
    # pattern = re.compile(r'<ul id="translateResult">\W*?<li>(.*?)</li>\W*?</ul>', re.S)
    html = rs.text.replace('\r\n', '')
    soup = BeautifulSoup(html, 'lxml')
    result = soup.select('#translateResult')
    return result[0].text.strip()


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
    rs = requests.post(url, params=params, headers=headers, data=data, timeout=timeout)
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
    rs = requests.post(url, headers=headers, data=data, timeout=timeout)
    if rs.status_code != 200:
        print('请求错误代码: ', rs.status_code)
        return None
    return rs.json().get('translationResponse')


def cnkiTranslator(text, flg=0):
    if len(text) > 20:
        return 'too long for cnki!'
    url = 'http://dict.cnki.net/dict_result.aspx'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    params = {'searchword': text}
    rs = requests.get(url, params=params, headers=headers, timeout=timeout)
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
    rs = requests.get(url, headers=headers, params=params, timeout=timeout)
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
    text3 = '方便快捷地获取信息和服务'
    text4 = 'artificial'
    text5 = """Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800. It rose to dominate the personal computer operating system market with MS-DOS in the mid-1980s, followed by Microsoft Windows. The company's 1986 initial public offering (IPO), and subsequent rise in its share price, created three billionaires and an estimated 12,000 millionaires among Microsoft employees. Since the 1990s, it has increasingly diversified from the operating system market and has made a number of corporate acquisitions, their largest being the acquisition of LinkedIn for $26.2 billion in December 2016,[7] followed by their acquisition of Skype Technologies for $8.5 billion in May 2011.[8]

As of 2015, Microsoft is market-dominant in the IBM PC-compatible operating system market and the office software suite market, although it has lost the majority of the overall operating system market to Android.[9] The company also produces a wide range of other consumer and enterprise software for desktops and servers, including Internet search (with Bing), the digital services market (through MSN), mixed reality (HoloLens), cloud computing (Azure) and software development (Visual Studio).

Steve Ballmer replaced Gates as CEO in 2000, and later envisioned a "devices and services" strategy.[10] This began with the acquisition of Danger Inc. in 2008,[11] entering the personal computer production market for the first time in June 2012 with the launch of the Microsoft Surface line of tablet computers; and later forming Microsoft Mobile through the acquisition of Nokia's devices and services division. Since Satya Nadella took over as CEO in 2014, the company has scaled back on hardware and has instead focused on cloud computing, a move that helped the company's shares reach its highest value since December 1999.[12][13]

In 2018, Microsoft surpassed Apple as the most valuable publicly traded company in the world after being dethroned by the tech giant in 2010 """
    # print(langdetect(text2))
    # print(jinshanTranslator(text4, 1))
    # print(baiduTranslator(text))
    print(youdaoTranslator('主要是', 0))
    # print(bingTranslator(text))
    # print(googleTraslator(text2, 1))
    # print(cnkiTranslator('依托互联网数据资源和自然语言处理技术优势'))

