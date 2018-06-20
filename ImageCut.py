#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from PIL import Image


def check_image_path(path):
	if os.path.isfile(path):
		simage = Image.open(path)
		
		if simage:
			return simage
		else:
			return 
	else:
		print(path + 'is a directory not image')
		return 


	
def compress_image(simage, width, path):
	aimImg = simage.resize((width,width),Image.ANTIALIAS)
	name = 'icon-' + str(width) + '.png'
	path = path + '/' + name
	aimImg.save(path,'png')


def deal_cut(simage):
	path = new_file_path(savePath)
	os.mkdir(path)

	print(path)

	#目标尺寸数组
	arr = [20,29,40,41,42,58,60,80,120,180,512]
	for x in arr:
		compress_image(simage,x,path)


#获取唯一的文件夹名
def new_file_path(path):
	i = 1
	aimPath = path
    
	while os.path.exists(aimPath):
		i = i + 1
		arr = os.path.splitext(path)	#分割文件路径和文件类型，arr[0]为路径+文件名，arr[1]为文件类型
		aimPath = arr[0] + '-' + str(i) + arr[1]

	return aimPath


imagePath = raw_input("输入文件路径：").rstrip()

#arr用于存储路径
arr = os.path.split(imagePath)
savePath = arr[0]
savePath = os.path.join(savePath,os.path.splitext(arr[1])[0])

img = check_image_path(imagePath)

if not img is None:
	deal_cut(img)


