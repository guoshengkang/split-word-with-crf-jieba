#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os,sys
import string
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba

#替换结巴词库
dcit_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'dict.txt')
jieba.set_dictionary(dcit_path)

# 如果有一些词语需要合并可以添加个人词典
# jieba.load_userdict('userdict.txt')
# 创建停用词列表
def creadstoplist(stopwordspath):
    stwlist = [line.strip() for line in open(stopwordspath, 'r').readlines()]
    return stwlist

# 对句子进行分词
def seg_sentence(sentence): #输入unicode编码字符串
    sentence=sentence.upper() #将字母统一换成大写
    wordList = jieba.cut_for_search(sentence) #搜索引擎模式
    #停用词文件由用户自己建立,注意路径必须和源文件放在一起
    stwlist = creadstoplist('stopwords.txt') #这里加载停用词的路径
    stwlist.extend(list(string.lowercase+string.uppercase+string.punctuation+" "+'\t')) #添加英文标点符号
    keyword_list=[]
    digit_reg=r'^(\d+\.?\d*(?:L|ML|CM|MM|M|G|KG|V)?)$' #数字正则
    digit_reg=re.compile(unicode(digit_reg,'utf8'))
    for word in wordList:
        if word not in stwlist: #判断是否是停用词
            if len(word) >= 1:  # 去掉长度为1的词
                is_digit=re.search(digit_reg,word) #判断关键词是否为数字
                if is_digit is None:
                    keyword_list.append(word)
    return '|'.join(keyword_list)

