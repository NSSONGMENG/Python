# Python

>ios.py 遍历iOS（OC）工程中的所有.h和.m文件，将多语言LocalizedString(@"key")中的key取出并写入本地文件

>android.py 遍历安卓工程工程中的所有.java和.xml文件，筛选出所有用过的key写入本地，并删除多语言文件中未使用的key-value

>compare.py ios.py生成的文件和android.py修改的多语言文件进行对比，将异同输入到新的文件中
