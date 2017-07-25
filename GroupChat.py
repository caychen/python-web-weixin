#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: Webwx.GroupChat

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 群聊 

@version: 
'''

from Webwx.ChatWith import ChatWith

def GroupChat():
    from Webwx.LoginWebwx import bIsLogin
    if not bIsLogin:
        print('还未登录，请登录后群聊...')
        return
    
    from Webwx.LoginWebwx import groupContactList
    ChatWith(groupContactList, True)
