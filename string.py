#!/usr/bin/env python3

#
#	遍历工程中的所有文件，将多语言LocalizedString(@"key")中的key取出并写入本地文件
#	


import os
import time


#递归遍历文件夹
def traverse(path):
	fileList = os.listdir(path)

	for f in fileList:
		filePath = os.path.join(path,f)

		if os.path.isfile(filePath):
			#文件
			readFile(filePath)
		else:
			#递归遍历路径
			traverse(filePath)


#读取文件
def readFile(path):
    #仅仅对.h和.m文件进行操作
    str = os.path.splitext(path)[1]

    if str == '.m' or str == '.h':
    	#文件名
    	fileName = os.path.split(path)[1]
    	fileName = os.path.splitext(fileName)[0]

    	stringList = []
    	if fileName in aimDic:
    		stringList = aimDic[fileName]

    	with open(path,'r') as f:
    		#读操作
    		rows = f.readlines()
    		for row in rows:
    			if 'LocalizedString' in row:
    				cutString(row,stringList)

    	if len(stringList) > 0:
    		aimDic[fileName] = stringList
    		print(' ----- ' + fileName + ' ----- ')



#截取目标字符串，保存在dic中，利用dic去重
def cutString(string,stringList):
	string = string.strip()		#去除\n
	string = string.lstrip()	#去除左边空格

	#根据LocalizedString切片
	parts = string.split('LocalizedString')

	for tmp in parts:
		if '(@' in tmp:
			#print(tmp)
			subParts = tmp.split('")')
			tmp = subParts[0]
			subParts = tmp.split('(@"')
			tmp = subParts[1]
			if not tmp in tmpDic:
				stringList.append(tmp)
				tmpDic[tmp] = tmp


#将dic中的key-value写入文件
def writeToFile(dic,path,strCount,fileCount):
    #设置文件名
	path = path + '/' + 'aimString.txt'
	#获取唯一的文件名
	path = newFilePath(path)

	with open(path,'w') as f:
		#写入时间
		f.write('//创建时间 '+time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))

		for (key,strList) in dic.items():
			string = '\n\n\n//------------ ' + key + ' ------------\n\n'
			f.write(string)

			strList.sort(key=lambda x:len(x),reverse=False)
			for string in strList:
				# eg. "没有绑定银行卡" = "没有绑定银行卡";
				string = '"' + string + '"' + ' = ' + '"' + string + '"' + ';' + '\n'
				f.write(string)
                
	#写操作结束
	print("共",fileCount,"个文件",strCount,"条数据，已写入：",path)


#获取唯一的文件名
def newFilePath(path):
	i = 1
	aimPath = path
    
	while os.path.exists(aimPath):
		i = i + 1
		arr = os.path.splitext(path)	#分割文件路径和文件类型，arr[0]为路径+文件名，arr[1]为文件类型
		aimPath = arr[0] + str(i) + arr[1]

	return aimPath
		


# --------------- 以下为主操作 ---------------
path = input("输入工程路径:")

print('...')
print('...')

path = path.rstrip()	#去除右边空格
#全局dic，存储所有key，达到去重的目的
tmpDic = {} 	
#全局dic，存储每个文件及其对应的目标字符串
aimDic = {}
traverse(path)
writeToFile(aimDic,path,len(tmpDic),len(aimDic))

print('🚀')
print('🚀🚀')
print('🚀🚀🚀')
