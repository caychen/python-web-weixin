#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: Webwx.ExitWebwx

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 正常退出

@version: 
'''
import sys
import json

'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxlogout?redirect=xxx&type=xxx&skey=xxx&pass_ticket=xxx
        params:
            sid:xxx
            uin:xxx
'''
def ExitWebwx():
    '''
        Logout the webwx and notify the phone to quit. 
    '''
    from Webwx.LoginWebwx import bIsLogin
    if bIsLogin:
        from Webwx.LoginWebwx import session,base_uri, skey, pass_ticket,wxsid, wxuin
        url = base_uri + '/webwxlogout?redirect=%s&type=%s&skey=%s&pass_ticket=%s' % ('1','0',skey,pass_ticket)
        params = {'sid':wxsid,
                  'uin':wxuin
                  }
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        session.post(url, data=json.dumps(params), headers=headers)
        session = None
        print('退出web微信成功...')
        
    sys.exit()
    