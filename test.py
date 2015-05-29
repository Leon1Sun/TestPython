__author__ = 'Leon'
#coding=utf-8
import re
str = '\<b\>本年薪金：2143万美元\<\/b\>'
arr = re.findall('\d*万美元',str,re.S)
print arr[0]