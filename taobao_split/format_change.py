#!/usr/bin/python
# coding=utf-8
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
train_file1_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "test_file_with_no_id")
fin=open(train_file1_path)
train_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "test_file")
fout=open(train_file_path,'w')
id=10
fout.write(str(id)+'\tid\tid'+'\n')
for line in fin:
  fout.write(line)
  if len(line)==1:
    id=id+1
    if id>=100:
      id=10
    fout.write(str(id)+'\tid\tid'+'\n')
fout.close()
