#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def str_judgement(check_str):
    result=[]
    for char in check_str:
        if u'\u4e00' <= char <= u'\u9fff':
            char_type="ch"
        elif char >= u'\u0030' and char<=u'\u0039':
            char_type="num"
        elif (char >= u'\u0041' and char<=u'\u005a') or (char >= u'\u0061' and char<=u'\u007a'):
            char_type="alph"
        else :
            char_type="other"
        result.append(char_type)
    return result

def modified_to_column(source_file, file_to_write):
    f = open(file_to_write, 'w')
    with open(source_file) as fs:
        for line in fs:
            line = unicode(line.strip("\n"),"utf-8")
            line = line.split(',')
            if len(line) != 2:
                continue
            char_list = line[1].split('|')
            # print char_list
            for i in char_list:
                char_len = len(i)
                if char_len == 1:
                    identifier_list = ['s']
                elif char_len == 2:
                    identifier_list = ['b', 'e']
                else:
                    identifier_list = ['b']
                    for j in range(char_len-2):
                        identifier_list.append('m')
                    identifier_list.append('e')
                # print "identifier_list", identifier_list
                symbol_list = str_judgement(i)
                # print "symbol_list", symbol_list
                for index in range(char_len):
                    str_to_write = i[index]+'\t'+symbol_list[index]+'\t'+identifier_list[index]+'\n'
                    f.write(str_to_write)
            f.write('\n')

source_file = 'splitted_title_4_train'
file_to_write = 'train_file_with_no_id'
modified_to_column(source_file, file_to_write)