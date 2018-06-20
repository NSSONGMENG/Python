#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, itchat
from itchat.content import *



def login():
	print('login success!!!')

@itchat.msg_register(TEXT,isFriendChat=True,isGroupChat=True)

def handle_receive_message(msg):
	if msg['Type'] == 'Text':
		friend = itchat.search_friends(userName=msg['FromUserName'])

		print friend['DisplayName']
		if "关机" in msg['Text']:
			os.system('shutdown -h 100')


itchat.auto_login()
#friends = itchat.get_friends()
#print friends

itchat.run()




