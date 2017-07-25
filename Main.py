#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: WebWeiXin.Main

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: Main code. 

@version: 
'''

'''
     遗留问题：
    1、无法获取群组中各个群成员的性别，否则可以在添加好友的时候指定添加好友的性别；
    2、在发送信息的时候暂时只能使用英文，而无法发送中文；
    3、在一键加好友的模块中，如果长时间添加好友的话，接下来再发送加好友的请求会发送失败，应该是被Tencent发现频繁加好友而限制了，不过隔天就又能正常加好友了；
    4、发送消息的模块好像不是很稳定，有待优化。
'''

Menus = ['登录微信', '添加好友', '群聊', '私聊', '退出微信']
jpgFile = 'qrcode.jpg'

def ShowMenu():
    '''
        Show the main menu for user to select the option.
    '''
    print('*' * 6 + '菜单' + '*' * 6)
    for index, menu in enumerate(Menus):
        print(' ' * 3 + '(' + str(index + 1) + '): ' + menu + ' ' * 3)
    

if __name__ == '__main__':
    '''
        Main code.
    '''
    from Webwx.LoginWebwx import LoginWebWx
    from Webwx.AddFriends import AddFriends
    from Webwx.GroupChat import GroupChat
    from Webwx.PersonalChat import PersonalChat
    from Webwx.ExitWebwx import ExitWebwx
    
    while True:
        ShowMenu()
        try:
            index = input('选择序号: ').strip().lower()
            if index == '':
                raise KeyError
            
            index = int(index)
            if index in list(range(1, len(Menus) + 1)):
                {
                     1:LoginWebWx,  #LoginWebWx
                     2:AddFriends,  # AddFriend,
                     3:GroupChat,  # GroupChat,
                     4:PersonalChat,  # PersonalChat,
                     5:lambda:ExitWebwx()  # sys.exit
                }[index]()
        except (KeyError,InterruptedError):
            print('Enter error...')
        except Exception as reason:
            print(reason)
            ExitWebwx()
        
