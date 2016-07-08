#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Built-in
import re
import json
import os
import sys
from datetime import datetime
#from pprint import pprint
from functools import wraps

# third
import requests
from bs4 import BeautifulSoup
import jieba

# modules
from auth import Logging
from auth import ValidationError


class Kind(object):

    def __init__(self):
        self.job_list = ['houduankaifa', 'yidongkaifa', 'qianduankaifa', 'ceshi', 'yunwei', 'DBA', 'gaoduanjishuzhiwei',
                         'yingjiankaifa2', 'qiyeruanjian']
        self.job_list_prefix = 'http://www.lagou.com/zhaopin/'

    def parse(self):
        self.job_list_url = [self.job_list_prefix +
                             temp for temp in self.job_list]
        for job_list in self.job_list_url:
            pass


class User(object):

    def __init__(self):
        pass  # 主要是如果用户登陆的话，可以取得想要查看的结果。该项工作的优先级可以往后放


class Job(object):

    job_prefix = 'http://www.lagou.com/jobs/'

    def __init__(self, url=None, position_id=None):
        if url:
            self.url = url
        if not hasattr(self, 'url'):
            self.url = job_prefix + '/' + str(position_id) + '.html'

    def parse(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, 'lxml')

    def parse_handle(func):
        @wraps(func)
        def func_wrapper(self):
            if not hasattr(self, 'soup'):
                self.parse()
            return func(self)
        return func_wrapper

    @parse_handle
    def get_title(self):
        soup = self.soup
        try:
            title = soup.find_all('h1')[1]['title']
        except AttributeError as ex:
            Logging.error(u'无法解析职位名称')
            Logging.error(ex)
            title = None
        return title

    @parse_handle
    def get_company(self):
        soup = self.soup
        try:
            company = re.sub(
                r'\s+', '', soup.find('h2', class_='fl').get_text())
            # 这里应该还有更好的方法来取得公司名称，不包括’未认证‘的内容
        except AttributeError as ex:
            Logging.error(u'无法解析公司名称')
            Logging.error(ex)
            company = None
        return company

    @parse_handle
    def get_description(self):
        soup = self.soup
        try:
            description = soup.find(
                'dd', class_='job_request').find_all('span')
            salary = description[0].string
            location = description[1].string
            experience = description[2].string
            education = description[3].string
            jtype = description[4].string
        except IndexError, AttributeError:
            Logging.error(u'无法解析职位信息')
            Logging.error(ex)
            raise ValueError('{} can\'t be resolved'.format(self.url))

        return salary, location, experience, education, jtype

    @parse_handle
    def get_request(self):
        soup = self.soup
        keyword = []

        request = soup.find('dd', class_='job_bt').find_all('p')

        for req in request:
            keyword.append(req.get_text())
        result = set()
        for kw in keyword:
            res = jieba.cut(kw)
            for r in res:
                temp = r.encode('ascii', 'ignore')
                if temp == '' or temp.isdigit() or temp == ',' or temp == '/':
                    continue
                result.add(r)

            # result.update([r.lower() for r in res if (r.encode('ascii','ignore')!='' and \
                # not r.encode('ascii','ignore').isdigit())]) one-line not
                # satisfy

        return result


class Company(object):
    # 这一部分是对公司进行评价

    def __init__(self, url=None, slug=None):
        company_prefix = 'http://www.lagou.com/gongsi/'
        if slug:
            self.url = company_prefix + str(slug) + '.html'
        else:
            self.url = url  # No Validation 未进行验证

    def parse(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content,"lxml")

    def parse_handle(func):
        @wraps(func)
        def func_wrapper(self):
            if not hasattr(self, 'soup'):
                self.parse()
            return func(self)
        return func_wrapper

    @parse_handle
    def get_name(self):
        soup=self.soup
        try:
            name = soup.find('div', class_='company_main').find(
                'h1').get_text()
            re.sub(r'\s+','',name)
        except AttributeError:
            raise ValidationError('u')
        return name # 还有换行符没有处理好，sigh……

    @parse_handle
    def get_information(self):
        soup=self.soup
        try:
            information=soup.find('div',id='basic_container').find_all('li')
            prof=information[0].find('span').string
            equity=information[1].find('span').string
            scale=information[2].find('span').string
            location=information[3].find('span').string
        except AttributeError,IndexError:
            raise Validation(u'some happened')
        return prof,equity,scale,location



def main():
    # url='http://www.lagou.com/zhaopin/houduankaifa'
    url = 'http://www.lagou.com/jobs/positionAjax.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
        'Host': 'www.lagou.com',
        'Origin': 'http://www.lagou.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    params = {
        'needAdditionalResult': 'False'
    }
    data = {
        'first': 'False',
        'pn': 320,
        'kd': '后端开发'
    }
    # params=json.dumps(params)
    try:
        r = requests.post(url, headers=headers, params=params, data=data)
        print r.url
        for i in r.json()['content']['positionResult']['result']:
            print i['positionId']
    except TypeError, ValueError:
        Logging.error(u'page out of range')
    '''
    with open('res.json','w+') as f:
        f.write(r.content)
    '''

if __name__ == '__main__':
    # main()
    '''
    job = Job(url='http://www.lagou.com/jobs/1806035.html')
    print job.get_title()
    print job.get_company()
    for i in job.get_description():
        print i
    print job.get_request()
    '''
    c = Company(slug=132600)
    print c.get_name()
    for i in c.get_information():
        print i
