#!/usr/bin/env python
# -*- coding:utf-8 -*-


from lagou import User,Company,Job
from auth import Logging,ValidationError
import requests
import cookielib

requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    pass


def crawl():
    
    # 使用 multiprocess 来进行多线程抓取
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
        'Host': 'www.lagou.com',
        'Origin': 'http://www.lagou.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    r=requests.get('http://www.lagou.com/s/subscribe.html',headers=headers)
    with open ('fuck.json','w+') as f:
        f.writelines(r.content)

    # 关于 Cookies 的使用再看一遍 requests 的文档 yeah！！

if __name__=='__main__':
    crawl()