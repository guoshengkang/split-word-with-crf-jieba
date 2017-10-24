★★★★★TASK1:训练CRF++模型★★★★★
【Step1】:抽取样本500000(raw_title文件),采用阿里分词api进行分词
新建空文件:splitted_title
code:taobao_split_word.py
分词结果保存至:splitted_title
分成训练和测试两个文件:splitted_title_4_train和splitted_title_4_test
【Step2】:将分词结果转化为CRF++的训练数据
运行splitted_to_train.py 修改splitted_title_4_train文件的格式,输出train_file_with_no_id
运行format_change.py 修改文件train_file_with_no_id,输出train_file
同样的方法,产生测试文件test_file

【Step3】:将400000条数据作为CRF++训练模型,将100000条作为测试数据
将CRF++-0.58文件夹下的crf_learn和crf_test设为环境变量
注:若在linux环境运行命令行, 保证train_file和test_file均为unix格式
训练模型命令:crf_learn -f  3 -c 2.5 -p 4 template train_file model
测试模型命令:crf_test -m model test_file >> test_result.txt
统计测试结果命令:./conlleval.pl -d "\t" < test_result.txt

【Step4】:根据测试结果,选择一个准确率(accuracy)最高的模型
方法:参数设置从大范围找到峰值,然后缩小至峰值周围寻找最优参数

---------------------------------------------------------------------

★★★★★TASK2:产生jieba词库★★★★★
【Step1】:选取100000数据,使用CRF++模型进行分词;
insert overwrite local directory '/home/kangguosheng/tmp'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE
select *
from tmp_kgs_new_titles
order by rand()
limit 100000;

【Step2】:将分词结果进行统计词频;
code:freq_stat.py

【Step3】:将频次出现超过一次的词语作为jieba的词库.

----------------------------------------------------------------------

★★★★★TASK3:CRF++&结巴分词★★★★★
【Step1】:获取idl_title_agg表中所有数据(7575857条),形成5个数据文件;
set mapreduce.job.reduces=5;
insert overwrite local directory '/home/kangguosheng/tmp'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE
DISTINCT char_id,char_raw
FROM idl_title_agg;

【Step2】:对5个数据文件进行-CRF++&结巴分词;
code:main.py/split_word.py
000000-->000000_output
000001-->000001_output
000002-->000002_output
000003-->000003_output
000004-->000004_output
注:可以四个线程同时开
另:提交文件不能超过100M,可以通过linux传送文件,命令如下:
将本地文件拷贝到远程
scp -i password_file copy_file kangguosheng@54.222.159.84:/home/kangguosheng
从远程将文件拷回本地
scp -i kangguosheng kangguosheng@54.222.159.84:/home/kangguosheng/tmp/000000_0 /home/kang/Desktop


【Step3】:将5个分词结果分别导入hive表的5个分区;
注:导入前,保证文件编码格式为utf-8
load data local inpath '/home/kangguosheng/000000_output' 
overwrite into table tmp_kgs_crf_jieba partition(ds='00');

drop table tmp_kgs_crf_jieba;
CREATE TABLE tmp_kgs_crf_jieba
(
title_id STRING COMMENT 'title ID',
crf_token STRING COMMENT 'crf_token',
jieba_token STRING COMMENT 'jieba_token'
)
comment "crf_jieba_split"
PARTITIONED BY (ds STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE;

【Step4】:将tmp_kgs_crf_jieba表的数据导入到idl_title_crf_jieba_agg表中.
drop table idl_title_crf_jieba_agg;
CREATE TABLE idl_title_crf_jieba_agg
(
title_id STRING COMMENT 'title ID',
crf_token ARRAY<STRING> COMMENT 'crf_token',
jieba_token ARRAY<STRING> COMMENT 'jieba_token'
)
comment "crf_jieba_split"
PARTITIONED BY (ds STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE;

ALTER TABLE idl_title_crf_jieba_agg DROP PARTITION (ds="2017-10-20" );
INSERT INTO idl_title_crf_jieba_agg PARTITION (ds="2017-10-20")
SELECT 
title_id,
split(crf_token,'\\|') AS crf_token,
split(jieba_token,'\\|') AS jieba_token
FROM tmp_kgs_crf_jieba;

