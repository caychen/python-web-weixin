#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: Webwx.AddFriends

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 

@version: 
'''
import time
import json
    

'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxverifyuser?r=xxx%s&pass_ticket=xxx
        params:
            r:timestamp
            pass_ticket:xxx
            BaseRequest:
            {
                DeviceID:'xxx',
                Sid:'xxx',
                Skey:'xxx',
                Uin:'xxx'
            }
            Opcode:2,常量，不知什么意思？
            SceneList:[33],列表,其中33代表什么意思？
            SceneListCount:1,未知，不知什么意思？
            VerifyContent:添加好友时要发送的验证信息
            VerifyUserListSize:1,代表每次添加一个
            skey:xxx
            VerifyUserList:
            {
                Value:要添加的好友的UserName
                VerifyUserTicket:''
            }
'''
def __Add(username=None):
#     print(username)
    from Webwx.LoginWebwx import base_uri, pass_ticket, BaseRequest, skey, session
    url = base_uri + '/webwxverifyuser?r=%s&lang=zh_CN&pass_ticket=%s' % (int(time.time()), pass_ticket)
    headers = {
               'Content-Type':'application/json;charset=utf-8',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:48.0) Gecko/20100101 Firefox/48.0',
               'Accept':'application/json, text/plain, */*'}
    params = {
              'BaseRequest':BaseRequest,
              'Opcode' : 2,
              'SceneList':[33],
              'SceneListCount':1,
              'VerifyContent':'Hello',
              'VerifyUserListSize':1,
              'skey':skey,
              'VerifyUserList':{
                                   'Value':username,
                                   'VerifyUserTicket':''
                                }
    }
    
    try:
        resp = session.post(url=url, data=json.dumps(params), headers=headers)
        data = resp.json()
        return data['BaseResponse']['Ret']
    except Exception as reason:
        print(reason)
        return '-1'
    

'''
    List the groupList or userList
'''
def ListUser(userOrGrouplist, bGroup):
    if bGroup:
        for index, userOrGroup in enumerate(userOrGrouplist):
            print('{0}: {1}\t{2}人\t'.format(index + 1, userOrGroup['NickName'], userOrGroup['MemberCount']))  # index + 1, ':\t', userOrGroup['NickName'], '\t', str(userOrGroup['MemberCount']) + '人')
    else:
        for index, userOrGroup in enumerate(userOrGrouplist):
            print('{0}: {1}'.format(index + 1, userOrGroup['NickName']))  # index + 1, ':\t', userOrGroup['NickName'], '\t')
        

#添加群组中的非好友的主函数
def AddFriends():
    '''
        Add the friends in the one group which is selected by user.
    '''
    from Webwx.LoginWebwx import bIsLogin, groupContactList, friends, Myself
    
    if not bIsLogin:
        print('还未登录，请登录后添加好友...')
        return
    
    ListUser(groupContactList)
    
    while True:
        try:
            index = input('输入编号(输入0结束)：')
            if index.strip()[0] == '0':
                break
            elif int(index.strip()) > len(groupContactList):
                raise IndexError('out of range: %s' % index)
            
            group = groupContactList[int(index) - 1]
            memberList = group['MemberList']
            UserNames = [friend['UserName'] for friend in friends]
                        
            for member in memberList:
#                 print(member['UserName'], member['NickName'])
                if member['UserName'] in UserNames:
                    print('\t%r已是%r好友...' % (member['NickName'], Myself['NickName']))
                elif member['UserName'] == Myself['UserName']:  # 自己
                    pass
                else:
#                     print(member['NickName'])
                    if __Add(member['UserName']) == 0:
                        print('\t%r请求加%r为好友，请求信息发送成功...' % (Myself['NickName'], member['NickName']))
                    else:
                        print('\t%r请求加%r为好友，请求信息发送失败...' % (Myself['NickName'], member['NickName']))
                    time.sleep(10)
            else:
                print('%r群组请求完成...' % (group['NickName']))
        except (KeyboardInterrupt, IndexError) as e:
            print(e)
            
