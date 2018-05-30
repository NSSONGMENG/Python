#!/usr/bin/env python3

import os
import difflib



str1 = input("字符串1: ")
str2 = input("字符串2: ")

#文本相似度
print(difflib.SequenceMatcher(None,str1,str2).quick_ratio())




