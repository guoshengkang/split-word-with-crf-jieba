#!/usr/bin/python
# coding=utf-8

__author__ = 'wumoumou'

import sys,os,re,string,time,json,gzip,random,pprint
from split_word import *
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

def remove_stopwords(keyword_list): #去重并去停用词
  keyword_list=list(set(keyword_list)) #去重
  stwlist = creadstoplist('stopwords.txt') #这里加载停用词的路径
  stwlist.extend(list(string.digits+string.lowercase+string.uppercase+string.punctuation+" "+'\t')) #添加英文标点符号 
  digit_reg=r'^(\d+\.?\d*(?:L|ML|CM|MM|M|G|KG|V)?)$' #数字正则
  digit_reg=re.compile(unicode(digit_reg,'utf8'))
  unique_keyword=[]
  for keyword in keyword_list: #去停用词
    if keyword not in stwlist: #判断是否是停用词
      if len(keyword) > 1:
        is_digit=re.search(digit_reg,keyword) #判断关键词是否为数字
        if is_digit is None: #不是全数字
          unique_keyword.append(keyword)
      else:
        unique_keyword.append(keyword)
  return unique_keyword

def main():
  for k in range(5): # 0-1
    print 'the %dth file is started!!!'%k
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fin_name='00000'+str(k)
    fout_name=fin_name+'_output'
    fin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], fin_name)
    fin=open(fin_path,'r')
    fout_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], fout_name)
    fout=open(fout_path,'w')
    while True:
      line = fin.readline()
      if not line:
          break
      line=line.strip()
      inputs={}    
      title_id,title=line.split(',')
      inputs[title_id]=title
      crf_result,jieba_result= run_task(inputs)
      crf_dict=json.loads(crf_result)
      jieba_result=json.loads(jieba_result)
      for key in crf_dict:
        crf_unique_keyword=remove_stopwords(crf_dict[key].split(unicode('|','utf-8')))
        crf_str='|'.join(crf_unique_keyword)
        new_line=','.join([key,crf_str,jieba_result[key]])
        fout.write(new_line.encode('utf-8')+'\n')
    fin.close()
    fout.close()
    print 'the %dth file is done!!!'%k
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

if __name__ == '__main__':
  starttime = datetime.datetime.now()    
  # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
  main()
  # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
