������TASK1:ѵ��CRF++ģ�͡�����
��Step1��:��ȡ����500000(raw_title�ļ�),���ð���ִ�api���зִ�
�½����ļ�:splitted_title
code:taobao_split_word.py
�ִʽ��������:splitted_title
�ֳ�ѵ���Ͳ��������ļ�:splitted_title_4_train��splitted_title_4_test
��Step2��:���ִʽ��ת��ΪCRF++��ѵ������
����splitted_to_train.py �޸�splitted_title_4_train�ļ��ĸ�ʽ,���train_file_with_no_id
����format_change.py �޸��ļ�train_file_with_no_id,���train_file
ͬ���ķ���,���������ļ�test_file

��Step3��:��400000��������ΪCRF++ѵ��ģ��,��100000����Ϊ��������
��CRF++-0.58�ļ����µ�crf_learn��crf_test��Ϊ��������
ע:����linux��������������, ��֤train_file��test_file��Ϊunix��ʽ
ѵ��ģ������:crf_learn -f  3 -c 2.5 -p 4 template train_file model
����ģ������:crf_test -m model test_file >> test_result.txt
ͳ�Ʋ��Խ������:./conlleval.pl -d "\t" < test_result.txt

��Step4��:���ݲ��Խ��,ѡ��һ��׼ȷ��(accuracy)��ߵ�ģ��
����:�������ôӴ�Χ�ҵ���ֵ,Ȼ����С����ֵ��ΧѰ�����Ų���

---------------------------------------------------------------------

������TASK2:����jieba�ʿ������
��Step1��:ѡȡ100000����,ʹ��CRF++ģ�ͽ��зִ�;
insert overwrite local directory '/home/kangguosheng/tmp'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE
select *
from tmp_kgs_new_titles
order by rand()
limit 100000;

��Step2��:���ִʽ������ͳ�ƴ�Ƶ;
code:freq_stat.py

��Step3��:��Ƶ�γ��ֳ���һ�εĴ�����Ϊjieba�Ĵʿ�.

----------------------------------------------------------------------

������TASK3:CRF++&��ͷִʡ�����
��Step1��:��ȡidl_title_agg������������(7575857��),�γ�5�������ļ�;
set mapreduce.job.reduces=5;
insert overwrite local directory '/home/kangguosheng/tmp'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE
DISTINCT char_id,char_raw
FROM idl_title_agg;

��Step2��:��5�������ļ�����-CRF++&��ͷִ�;
code:main.py/split_word.py
000000-->000000_output
000001-->000001_output
000002-->000002_output
000003-->000003_output
000004-->000004_output
ע:�����ĸ��߳�ͬʱ��
��:�ύ�ļ����ܳ���100M,����ͨ��linux�����ļ�,��������:
�������ļ�������Զ��
scp -i password_file copy_file kangguosheng@54.222.159.84:/home/kangguosheng
��Զ�̽��ļ����ر���
scp -i kangguosheng kangguosheng@54.222.159.84:/home/kangguosheng/tmp/000000_0 /home/kang/Desktop


��Step3��:��5���ִʽ���ֱ���hive���5������;
ע:����ǰ,��֤�ļ������ʽΪutf-8
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

��Step4��:��tmp_kgs_crf_jieba������ݵ��뵽idl_title_crf_jieba_agg����.
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

