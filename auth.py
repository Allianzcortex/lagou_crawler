#!/usr/bin/env python
# -*- coding:utf-8 -*-

import termcolor

class Logging(object):

    @staticmethod
    def error(msg):
        print ''.join([termcolor.colored('error','red'),':',termcolor.colored(msg,'white')])

    @staticmethod
    def success(msg):
        print ''.join([termcolor.colored('success','green'),':',termcolor.colored(msg,'white')])

    @staticmethod
    def info(msg):
        print ''.join([termcolor.colored('info','magenta'),':',termcolor.colored(msg,'white')])

class ValidationError(Exception):

    def __init__(self,message):
        self.message=message
        Logging.error(message)

if __name__=='__main__':
    pass