#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: Main.LoginWebwx

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 登录web微信模块

@version: 
'''
import time
import re
import os
import xml.dom.minidom
import json
import requests

from Webwx.Main import  jpgFile

tip = 0
uuid = ''
redirect_uri = ''
base_uri = ''
push_uri = ''
skey = ''
wxsid = ''
wxuin = ''
pass_ticket = ''

ContactList = []
Myself = []
SyncKey = []
BaseRequest = None
groups = []
friends = []
groupContactList = []
session = None

bIsLogin = False

'''
    Interface:
        url:
            https://login.weixin.qq.com/jslogin
        params:
            appid : 'wx782c26e4c19acffb'，应用ID（固定值）
            fun : 'new'
            lang : 'en_US' 或' zh_CN'，浏览器的语言
            _ : timestamp时间戳，表示当前时间
'''
def __GetUUID():
    '''
        Get the UUID for obtaining the qrcode
    '''
    url = 'https://login.weixin.qq.com/jslogin'
    params = {
               'appid': 'wx782c26e4c19acffb',  # 应用id，固定值
               'fun': 'new',  # 固定值
               'lang': 'zh_CN',  # 浏览器的语言
               '_': int(time.time())  # 时间戳
    }
    global session, uuid
    session = requests.session()
    resp = session.get(url=url, params=params)
    resp.encoding = 'utf-8'
    reg = re.search(r'indow.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"', resp.text)
#     print(reg.group(1))
#     print(reg.group(2))

    uuid = reg.group(2)
    
    if reg.group(1) == '200':
        return True
    return False


'''
    Interface:
        url:
            https://login.weixin.qq.com/qrcode/uuid
        params:
            t : 'webwx',固定值
            _ : timestamp时间戳
        
'''
def __GetCode():
    '''    
        Show the image which contains the qrcode icon.
    '''
    if __GetUUID() == True:
        print('正在获取二维码图片...')
        url = 'https://login.weixin.qq.com/qrcode/' + uuid
        params = {
                 't': 'webwx',  # fixed value
                 '_': int(time.time()),  # timestamp
        }
        
        response = session.get(url=url, params=params)
        with open(jpgFile, 'wb') as f:
            f.write(response.content)
        
    #     os.startfile('qrcode.jpg')#equals to next line
        os.popen(jpgFile)  # open the imgfile
    
    else:
        return
    
    
'''
    Interface:
        url:
            https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login
        params:
            tip : 1:未扫描, 0:已扫描
            uuid : 获取到的uuid
            _ : 时间戳
'''
def __WaitForLogin():
    '''
        Waiting for scanning the qrcode by phone.
    '''
    global tip
    
#     print(tip)
    url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
        tip, uuid, int(time.time()))
        
    resp = session.get(url=url)
#     print(resp.text)
    
    regx = re.search(r'window.code=(\d+)', resp.text)
    code = regx.group(1)
#     print(code)
    
    if code == '201':  # 已扫描，还未确定
        print('成功扫描,请在手机上点击确认以登录')
        tip = 0
        
    elif code == '200':  # 已确定登录
        print('正在登录...')
        global redirect_uri, base_uri
        redirect_uri = re.search(r'window.redirect_uri="(\S+?)";', resp.text).group(1) + '&fun=new&version=v2'
#         print(redirect_uri)
        base_uri = redirect_uri[:redirect_uri.rfind('/')]
            
    elif code == '408':
        pass
    
    return code  


'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage
        params:
            ticket:xxx
            uuid:xxx
            lang:xxx
            scan:扫码成功后返回的时间戳
            fun:'new'
            version:'v2'
    
    Attention: 该请求是在window.redirect_uri最后拼接'&fun=new&version=v2',而redirect_uri可以从用户确认登录成功后直接返回
'''
def __Login():
    '''
        Login the weixin web and obtain the parameters(uin、skey、sid、pass_ticket).
    '''
#     print(redirect_uri)
    xmldoc = session.get(url=redirect_uri).text
#     print(xmldoc)
    doc = xml.dom.minidom.parseString(xmldoc)
    root = doc.documentElement  # error根节点
    
    global skey, wxsid, wxuin, pass_ticket
    for node in root.childNodes:
        if node.nodeName == 'skey':
            skey = node.childNodes[0].data
        elif node.nodeName == 'wxsid':
            wxsid = node.childNodes[0].data
        elif node.nodeName == 'wxuin':
            wxuin = node.childNodes[0].data
        elif node.nodeName == 'pass_ticket':
            pass_ticket = node.childNodes[0].data
            
#     print(skey, wxsid, wxuin, pass_ticket)
    if not all((skey, wxsid, wxuin, pass_ticket)):
        return False

    return True


'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=xxx&pass_ticket=xxx&skey=xxx
        params:
            BaseRequest:
            {
                DeviceID:'xxx',
                Sid: 'xxx',
                Skey: 'xxx',
                Uin: 'xxx'
            }
'''
def __Webwxinit():
    '''
        Obtaining the initialized information(headers, friends ect.).
    '''
    url = base_uri + '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time()))
    headers = {'Accept':'application/json, text/plain, */*', 'Host':'wx2.qq.com'}
    
    global BaseRequest
    BaseRequest = {
               'DeviceID':'e000000000000000',  # e+15位随机数
               'Sid': wxsid,
               'Skey': skey,
               'Uin': int(wxuin)
    }
    params = {'BaseRequest': BaseRequest}
    
    resp = session.post(url=url, data=json.dumps(params), headers=headers)
    resp.encoding = 'utf-8'
    data = resp.json()  # json.loads(resp)
#     print(data)
    
    global ContactList, Myself, SyncKey
    '''
        ContactList为最近活跃的对象，其中Username来区分好友或者群组或者服务号，一个'@'为好友，两个'@'为群组，没有@的为服务号
        MPSubscribeMsg为公众号推送的阅读文章
        MPSubscribeMsgList:为公众号列表 及其推送的文章
        User其实就是自己账号信息（用在顶部的头像） 
    '''
    ContactList = data['ContactList']
    Myself = data['User']
    SyncKey = data['SyncKey']
    
    return __responseState('Webwxinit', data['BaseResponse'])
    
    
    
def __responseState(func_name, resp_Obj=None):
    Ret = resp_Obj['Ret']
    ErrMsg = resp_Obj['ErrMsg'] 
    
    if Ret != 0:
        print('func: %r, Ret: %d, ErrMsg: %r' % (func_name, Ret, ErrMsg))
        return False
    
    return True
    
    
'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact
        params:
            pass_ticket : xxx
            skey : xxx
            r : timestamp
'''    
def __GetUserList():
    '''
        Getting the friends.
    '''    
    url = base_uri + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time()))
    headers = {'content-type': 'application/json; charset=UTF-8'}
    resp = session.get(url, headers=headers)
    resp.encoding = 'utf-8'
    data = resp.json()
    
#     MemberCounts = data['MemberCount']
    MemberList = data['MemberList']  # 包括好友，群组和公众号
    
    __Classify(MemberList)
    
    
def __Classify(MemberList):  # 分类
    for member in MemberList:
        if member['UserName'].find('@@') != -1:  # 群聊
            groups.append(member)
        elif member['UserName'].find('@') != -1:  # 好友
            if member['VerifyFlag'] & 8 != 0:  # 公众号或者服务号
                pass
            elif member['UserName'] == Myself['UserName']:  # 自己
                pass
            else:  # 好友
                friends.append(member)
                
    
'''
    Interface:
        url:
            https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxbatchgetcontact?type=ex&r=xxx&pass_ticket=xxx
        params:
            BaseRequest:
            {
                DeviceID:'xxx',
                Sid:'xxx',
                Skey:'xxx',
                Uin:'xxx'
            }
            Count:参数List的长度
            List:对应于群组的信息，格式:{UserName：xxx，ChatRoomId/EncryChatRoomId:xxx}
            [
                0:{UserName: 'xxx', EncryChatRoomId: ''}
                1:{UserName: 'xxx', ChatRoomId: ''}
                …
            ]
'''    
def __Webwxbatchgetcontact():
    url = base_uri + '/webwxbatchgetcontact?type=ex&r=%s&pass_ticket=%s' % (int(time.time()), pass_ticket)
    headers = {'Content-Type':'application/json;charset=utf-8'}
    
    grouplist = []
    for group in groups:
#         print(({'UserName':group['UserName'], 'ChatRoomId':group['ChatRoomId']}))
        grouplist.append({'UserName':group['UserName'], 'ChatRoomId':group['ChatRoomId']})
        
    params = {'BaseRequest':BaseRequest,
              'Count':len(groups),
              'List':grouplist
              }
    resp = session.post(url=url, data=json.dumps(params), headers=headers)
    resp.encoding = 'utf-8'
    data = resp.json()
    
    global groupContactList
    groupContactList = [groupContact for groupContact in data['ContactList']]
#     print(len(groupContactList)) 


#登录微信模块的主函数
def LoginWebWx():
    __GetCode()
    print('请使用微信扫描二维码以登录...')
    while __WaitForLogin() != '200':
        pass
    else:
        print('确认登录...')
        os.remove(jpgFile)  # remove the qrcode image(qrcode.jpg)
    
    if __Login():
        print('登录成功...')
    else:
        print('登录失败')
        pass
    
    if __Webwxinit():
        print('初始化成功...')
    else:
        print('初始化失败...')
        pass
    
    __GetUserList()
    __Webwxbatchgetcontact()
    
    global bIsLogin
    bIsLogin = True
