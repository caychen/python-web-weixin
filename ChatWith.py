#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: Webwx.ChatWith

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 与好友/群组聊天主模块

@version: 
'''
from Webwx.AddFriends import ListUser
import json

#聊天主函数（接口）
def ChatWith(users=None, bGroup=False):
    ListUser(users, bGroup)
    
    while True:
        try:
            index = input('输入编号(输入0结束)：')
            if index.strip()[0] == '0':
                break
            elif int(index.strip()) > len(users):
                raise IndexError('out of range: %s' % index)
            
            user = users[int(index) - 1]
            
            __SendMessage(user)
        except (IndexError, KeyboardInterrupt) as reason:
            print(reason)
            

'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=xxx&pass_ticket=xxx
        params:
            BaseRequest:
            {
                DeviceID:'xxx',
                Sid:'xxx',
                Skey:'xxx',
                Uin:'xxx'
            }
            Msg:
            {
                Type:1,
                FromUserName:自己的UserName,
                ToUserName:发送信息给好友的UserName,
                LocalID:随机17位,
                ClientMsgId:同LocalID一样,
                Content:要发送的信息
            }
            Scene:0
'''            
def __SendMessage(user):
    '''
        Send message to the user or group.
    '''
    from Webwx.LoginWebwx import session, pass_ticket, base_uri, BaseRequest, Myself
    url = base_uri + '/webwxsendmsg?lang=%s&pass_ticket=%s' % ('zh_CN', pass_ticket)
    headers = {'Content-Type':'application/json;charset=utf-8',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:48.0) Gecko/20100101 Firefox/48.0'
    }
    
    params = {'BaseRequest':BaseRequest,
              'Msg':{'Type':1,
                     'FromUserName':Myself['UserName'],
                     'ToUserName':user['UserName'],
                     'LocalID':'00000000000000000',
                     'ClientMsgId':'00000000000000000'
                     },
              'Scene':0
              }
    
    while True:
        content = input('输入信息，以回车键发送(以q结束群聊): \n\t')
        if content.strip().lower()[0] == 'q':
            break
        
        params['Msg']['Content'] = content.strip()
        data = session.post(url, data=json.dumps(params), headers=headers).json()
        ret = data['BaseResponse']['Ret']
        if ret != 0:
            print('\t发送失败...')
                        
