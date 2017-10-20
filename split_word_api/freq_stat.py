#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,re
import sys
from jieba_cut import *
reload(sys)
sys.setdefaultencoding('utf-8')
from collections import defaultdict
frequencies = defaultdict(int) #传入int()函数来初始化

fin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "output")
fin=open(fin_path,'r')
fout_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "freq_stat.txt")
fout=open(fout_path,'w')

stwlist = creadstoplist('stopwords.txt') #这里加载停用词的路径
stwlist.extend(list(string.digits+string.lowercase+string.uppercase+string.punctuation+" "+'\t')) #添加英文标点符号

for line in fin:
  line=unicode(line.strip(), "utf-8")
  title_id,keyword_str= line.split(unicode(',','utf-8'),1)
  keyword_list=set(keyword_str.split(unicode('|','utf-8')))
  keyword_list=list(set(keyword_list)) #去重

  for keyword in keyword_list: #去停用词
    digit_reg=r'^(\d+\.?\d*(?:L|ML|CM|MM|M|G|KG|V)?)$' #数字正则
    digit_reg=re.compile(unicode(digit_reg,'utf8'))
    if keyword not in stwlist: #判断是否是停用词
      if len(keyword) > 1:
        is_digit=re.search(digit_reg,keyword) #判断关键词是否为数字
        if is_digit is None: #不是全数字
          frequencies[keyword]+= 1
      else:
        frequencies[keyword]+= 1

sorted_dict=sorted(frequencies.iteritems(), key=lambda d:d[1], reverse = True ) #d[0]为key,d[1]为value,返回一个元组列表
# need_num=int(len(sorted_dict)*0.5) #50%
for keyword,frequency in sorted_dict:
  new_line=' '.join([keyword,str(frequency)])
  fout.write(new_line.encode('utf-8')+'\n')

fin.close()
fout.close()

