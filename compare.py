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
					andDic[key] = val
	elif filtType == '.txt':
		with open(file,'r') as f:
			rows = f.readlines();
			for row in rows:
				if '" = "' in row:
					tmp = row.split('" = "')[0]
					tmp = tmp.split('"')[1]
					iosDic[tmp] = tmp


def compare_list():
	for (key,val) in andDic.items():
		if val in iosDic:
			bothDic[key] = val
			del iosDic[val]
		else:
			andLeft[key] = val

	print('ios特异：',len(iosDic))
	print('and特异：',len(andLeft))
	print('共同：',len(bothDic))


def write_to_file(path,name):
	#设置文件名
	path = path + '/' + name
	#获取唯一的文件名
	path = new_file_path(path)

	with open(path,'w') as f:
		#写入时间
		f.write('//创建时间 '+time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))

		#安卓
		f.write('\n\n\n // ----------- ' + str(len(andLeft)) + '条安卓特异 ----------- \n')
		for (key,val) in andLeft.items():
			f.write(key + ' = ' + val + '\n')

		#ios
		f.write('\n\n\n // ----------- ' + str(len(iosDic)) + ' ios特异 ----------- \n')
		for (key,val) in iosDic.items():
			f.write(key + ' = ' + val + '\n')

		#iOS安卓共用
		f.write('\n\n\n // ----------- ' + str(len(bothDic)) +  'iOS安卓共用 ----------- \n')
		for (key,val) in bothDic.items():
			f.write(key + ' = ' + val + '\n')   

	print('数据已写入：' + path)

#获取唯一的文件名
def new_file_path(path):
	i = 1
	aimPath = path
    
	while os.path.exists(aimPath):
		i = i + 1
		arr = os.path.splitext(path)	#分割文件路径和文件类型，arr[0]为路径+文件名，arr[1]为文件类型
		aimPath = arr[0] + str(i) + arr[1]

	return aimPath



print('......')

iosDic = {}	#ios语言脚本
andDic = {}	#安卓语言脚本

andLeft = {}	#安卓特异
bothDic = {}	#同时存在的key

path = input("输入文件路径：").rstrip()

read_path(path)
compare_list()
write_to_file(path,'aimStr')



print('ALL DONE')




