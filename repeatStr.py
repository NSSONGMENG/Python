#!/usr/bin/env python3

import os
import time
import difflib


def read_path(path):
	fileList = os.listdir(path)
	for f in fileList:
		filePath = os.path.join(path,f)
		if os.path.isfile(filePath):
			read_file(filePath)
		else:
			print(filePath)


def read_file(file):
	filtType = os.path.splitext(file)[1]
	print(filtType)
	if filtType == '.xml':
		with open(file,'r') as f:
			rows = f.readlines();
			for row in rows:
				if '<string name="' in row:
					key = row.split('">')[0]
					key = key.split('name="')[1]

					val = row.split('">')[1]
					val = val.split('</string>')[0]
					
					if val in totalDic:
						print(key + ' = ' + val)

					totalDic[val] = key




print('......')

totalDic = {}

path = input("输入文件路径：").rstrip()

read_path(path)


print('ALL DONE')




