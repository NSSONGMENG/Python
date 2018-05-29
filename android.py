#!/usr/bin/env python3

#
#	遍历工程中的所有文件，将多语言LocalizedString(@"key")中的key取出并写入本地文件
#	


import os
import time


#递归遍历文件夹
def traverse_path(path):
	fileList = os.listdir(path)

	for f in fileList:
		filePath = os.path.join(path,f)

		if os.path.isfile(filePath):
			#文件
			read_file(filePath)
		else:
			#递归遍历路径
			traverse_path(filePath)


#读取文件
def read_file(path):
    #仅仅对.h和.m文件进行操作
    str = os.path.splitext(path)[1]

    if str == '.xml' or str == '.java':
    	#文件名
    	fileName = os.path.split(path)[1]
    	fileName = os.path.splitext(fileName)[0]

    	if not fileName == 'merger':
	    	stringList = []
	    	if fileName in aimDic:
	    		stringList = aimDic[fileName]

	    	with open(path,'r') as f:
	    		#读操作
	    		rows = f.readlines()
	    		savePath = False
	    		for row in rows:
	    			if '@string/' in row or 'R.string.' in row or '<string name="' in row:
	    				cut_string(row,stringList)
	    			if '<string name="' in row and '/res/values/strings.xml' in path:
	    				savePath = True

	    		if savePath:
	    			xmlPath.append(path)

	    	if len(stringList) > 0:
	    		aimDic[fileName] = stringList
	    		print(' ----- ' + fileName + ' ----- ')


#截取目标字符串，保存在dic中，利用dic去重
def cut_string(string,stringList):
	string = string.strip()		#去除\n
	string = string.lstrip()	#去除左边空格

	#根据LocalizedString切片
	if '@string/' in string:
		parts = string.split('@string/')
		parts.pop(0)
		for tmp in parts:
			if '"/' in tmp:
				tmp = tmp.split('"/')[0].strip()
				cache_key(stringList, tmp)
			elif '"' in tmp:
				tmp = tmp.split('"')[0].strip()
				cache_key(stringList, tmp)
	elif 'R.string.' in string:
		parts = string.split('R.string.')
		parts = parts[1::1]
		for tmp in parts:
			for x in tmp:
				find = False
				if x == ')':
					tmp = tmp.split(')')[0].strip()
					cache_key(stringList, tmp)
					break
				elif x == ',':
					tmp = tmp.split(',')[0].strip()
					cache_key(stringList, tmp)
					break
	elif '<string name="' in string:
		tmp = string.split('<string name="')[1]
		if '">' in tmp:
			tmp = tmp.split('">')[0]
			lanDic[tmp] = tmp;


def cache_key(strList ,key):
	if not key in tmpDic:
		strList.append(key)
		tmpDic[key] = key


#将dic中的key-value写入文件
def write_key_to_file(path, name):
    #设置文件名
	path = path + '/' + name
	#获取唯一的文件名
	path = new_file_path(path)

	with open(path,'w') as f:
		#写入时间
		f.write('//创建时间 '+time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))

		for (key,strList) in aimDic.items():
			string = '\n\n\n//------------ ' + key + ' ------------\n\n'
			f.write(string)

			strList.sort(key=lambda x:len(x),reverse=False)
			for string in strList:
				# eg. "没有绑定银行卡" = "没有绑定银行卡";
				#string = '"' + string + '"' + ' = ' + '"' + string + '"' + ';' + '\n'
				string = string + '\n'
				f.write(string)
                
	#写操作结束
	print("共",len(aimDic),"个文件",len(tmpDic),"条数据，已写入：",path)


def write_unsless_file(path, name):
	#设置文件名
	path = path + '/' + name
	#获取唯一的文件名
	path = new_file_path(path)
	unfindList = []
	for (k,v) in tmpDic.items():
		if k in lanDic:
			del lanDic[k]
		else:
			unfindList.append(k)

	with open(path,'w') as f:
		f.write('//创建时间 '+time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + '\n\n\n')

		for str in unfindList:
			f.write('unfind key: ' + str)

		f.write('\n\n\n  ----------- 无用key -----------')
		for (k,v) in lanDic.items():
			f.write(k + '\n')

	print(len(unfindList),'条未添加key;',len(lanDic),'条无用key',"条数据，已写入：",path)



#获取唯一的文件名
def new_file_path(path):
	i = 1
	aimPath = path
    
	while os.path.exists(aimPath):
		i = i + 1
		arr = os.path.splitext(path)	#分割文件路径和文件类型，arr[0]为路径+文件名，arr[1]为文件类型
		aimPath = arr[0] + str(i) + arr[1]

	return aimPath


def remove_useless_key(filePathList):
	for path in filePathList:
		if os.path.isfile(path):
			print("修改多语言文件：" + path)
			lines = []
			with open(path,'r') as f:
				lines = f.readlines()

			with open(path,'w') as f:
				for line in lines:
					if '<string name="' in line:
						key = line.split('<string name="')[1]
						if '">' in key:
							key = key.split('">')[0]
						if key in lanDic:
							continue
						else:
							f.write(line)
					

	


# --------------- 以下为主操作 ---------------

path = input("输入工程路径:")
path = path.rstrip()	#去除右边空格

print('...')
print('...')

tmpDic = {} 	#全局dic，存储所有key，达到去重的目的
aimDic = {}		#全局dic，存储每个文件及其对应的目标字符串
lanDic = {}		#多语言dic
xmlPath = []	#list 保存多语言文件路径

#遍历工程目录，将所有用到的多语言保存在tmpDic中，aimDic中保存文件名极其对应的多语言列表
traverse_path(path)
#将用到的字符串，写入文件
write_key_to_file(path,'aimString.txt')
#将未用到的key写入文件
write_unsless_file(path,'useless.txt')
#在指定xml文件中删除未使用的key
remove_useless_key(xmlPath)

print('🚀')
print('🚀🚀')
print('🚀🚀🚀')
