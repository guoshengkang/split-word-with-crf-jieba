#!/usr/bin/python
# coding=utf-8

__author__ = 'wumoumou'

import sys,os,re,string,time,json,gzip,random
from jieba_cut import *
reload(sys)
sys.setdefaultencoding('utf8')

def random_str(randomlength=30):
    '''
    生成随机的字符串，用来作为文件名
    '''
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    randoms = random.Random()
    for i in range(randomlength):
        str+=chars[randoms.randint(0, length)]
    return str

def str_judgement(check_str):
    '''
    横行转换成竖行
    :param check_str:unicode类型的字符串
    :return:所属的字符类型列表
    '''
    result = []
    for char in check_str:
        if u'\u4e00' <= char <= u'\u9fff': #汉字
            char_type = "ch"
        elif char >= u'\u0030' and char <= u'\u0039': #数字
            char_type = "num"
        elif (char >= u'\u0041' and char <= u'\u005a') or (char >= u'\u0061' and char <= u'\u007a'): #字母
            char_type = "alph"
        else:
            char_type = "other" #其他
        result.append(char_type)
    return result 

def write_file(source_data, writefile_name_char):
    '''
    将文件内横行的数据(utf-8)转换成竖行的待分词数据(utf-8)
    :param source_data(字典格式{id:titel,....}:
    :param writefile_name_char:
    :return:char   type
    '''
    write_file_char = open(writefile_name_char, "w")
    for i in source_data:
        strs = unicode(source_data[i] , "utf-8") #title
        chars = i + "\t" + "id" + "\n" #e.g.,100   id
        write_file_char.write(chars) 
        g = str_judgement(strs) #判断字符类型,返回列表
        char_lens = len(strs)
        for j in xrange(char_lens):
            if strs[j] == " ":
                chars = "#" + "\t" + g[j] + "\n"
            elif g[j] == "alph":
                chars = string.upper(strs[j]).encode("utf-8") + "\t" + g[j] + "\n"
            else:
                chars = strs[j].encode("utf-8") + "\t" + g[j] + "\n"
            write_file_char.write(chars) #e.g.,大    ch
        write_file_char.write("\n")
    write_file_char.close()


def split_word(file_name,filename_split):
    '''
    功能:分词
    filename:char type
    :return:
    '''
    try:
        model_file = '%s/config/model' % sys.path[0]
        cmd = r'crf_test -m %s %s > %s' % (model_file, file_name, filename_split)
        cmd_result=os.system(cmd) #注意:在linux环境下才是成功
        if cmd_result==0:
            return True
        else:
            print "execute cmd_command error!!!"
            return False
    except Exception:
        return False


def create_sentence(file_name, word_col, tag_col, replace_word):
    '''
    竖行数据处理
    :param file_name:target_data
    :param word_col:字的位置
    :param tag_col:
    :param replace_word:
    :return:
    '''
    file_data = open(file_name, "r")
    result = {}
    keys = "-999999999" #默认key
    tmp = []
    wordseq = []
    while True:
        char_line = file_data.readline()
        if not char_line:
            if len(tmp) > 0:
                result.setdefault(keys, tmp)
            break
        char_line = unicode(char_line.strip("\n"), "utf-8")
        char_t = char_line.split("\t")
        if len(char_t)>1 and char_t[1] == 'id': #tag_col
            keys = char_t[0]
        else:
            if len(char_t) == 1:
                word = "".join(wordseq)
                if len(word) > 0:
                    tmp.append(word)
                    replace_words = replace_word.get(word)
                    if replace_words:
                        tmp.append(replace_words)
                if len(tmp) > 0:
                    tmp="|".join(tmp)
                    result.setdefault(keys, tmp)
                tmp = []
                wordseq = []
                continue
            else:
                if char_t[tag_col] in ("b", "s"):
                    word = "".join(wordseq)
                    if len(word) > 0:
                        tmp.append(word)
                        replace_words = replace_word.get(word)
                        if replace_words:
                            tmp.append(replace_words)
                    wordseq = []
                    wordseq.append(char_t[word_col])
                else:
                    wordseq.append(char_t[word_col])
    return result

def replace_word(file_name):
    file_data = open(file_name, "r")
    key_re = re.compile(r"(^.+):")
    value_re = re.compile(r":(.+$)")
    result = {}
    while True:
        char_line = file_data.readline()
        if not char_line:
            break
        char_line = unicode(char_line.strip("\n"), "utf-8")
        key_word = key_re.findall(char_line)
        value_word = value_re.findall(char_line)
        value_word = value_word[0].split(",")
        for i in value_word:
            result.setdefault(i, "^!" + key_word[0]) #替换词:"^!" + key_word[0]
    file_data.close()
    return result


def run_task(inputs):
    '''
    inputs:字典格式{id:titel,....}
    '''
    try:
        source_name = random_str()
        target_name = random_str()
        dir_path = os.getcwd()
        source_file = os.path.join(dir_path, "source_file", source_name)
        target_file = os.path.join(dir_path, "source_file", target_name)
        replace_file = os.path.join(dir_path, "config", "replace_word")
        replace_word_str = replace_word(replace_file) #读取替换词典
        write_file(inputs, source_file) #将字符串输出到文件:char type
        tag = split_word (source_file,target_file) #分词
        if tag:
            result_tmp = create_sentence(target_file, 0, 2, replace_word_str)
        else:
            result_tmp = {}
    except Exception as e:
        result_tmp = {}
        print 'crf++:err for %s' % e
    finally:
        if os.path.exists(source_file):
            os.remove(source_file)
        if os.path.exists(target_file):
            os.remove(target_file)
        crf_result=result_tmp
        # result = json.dumps(result_tmp, ensure_ascii=False)
        crf_result = json.dumps(result_tmp, ensure_ascii=False)
        
    try:
        result_tmp={}
        for title_id in inputs:
            sentence=unicode(inputs[title_id] , "utf-8")
            result_tmp[title_id]=seg_sentence(sentence)
    except Exception as e:
        result_tmp={}
        print 'jieba:err for %s' % e
    finally:
        jieba_result = json.dumps(result_tmp, ensure_ascii=False)

    return crf_result,jieba_result
