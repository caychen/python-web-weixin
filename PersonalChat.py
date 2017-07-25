#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: Webwx.PersonalChat

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 私聊

@version: 
'''
from Webwx.ChatWith import ChatWith

def PersonalChat():
    from Webwx.LoginWebwx import bIsLogin
    if not bIsLogin:
        print('还未登录，请登录后私聊...')
        return
    from Webwx.LoginWebwx import friends
    ChatWith(friends)#调用聊天主模块中的ChatWith，将第二个参数设为默认False，代表私聊
