#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib, urllib2, sys, json, traceback


def request_api(text):
    host = 'http://alinlp.market.alicloudapi.com'
    path = '/api/getnlpresult'
    appcode = '2917c1b4f324406593664efde339940c'
    querys = 'text=' + text
    url = host + path + '?' + querys

    request = urllib2.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    response = urllib2.urlopen(request, timeout=30)
    content = response.read()
    content = json.loads(content)
    result = ''
    for word in content['result']:
        word = word['word'].strip()
        if word == '' or word == None:
            continue
        result += word + '|'
    return result[:-1]

# print(request_api(u'修身棉衣'))

titles = {}
with open('raw_title','r') as raw_title:
    for title in raw_title:
        title = title.strip()
        if len(title.split(',')) == 2:
            titles[title.split(',')[0]] = title.split(',')[1]

with open('splitted_title','r') as splitted_title:
    for title in splitted_title:
        title = title.strip()
        title = title.split(',')
        if len(title) == 2 and titles.has_key(title[0]):
            del titles[title[0]]

with open('splitted_title','a') as splitted_title:
    for id,title in titles.items():
        try:
            title = title.replace(' ', '+')
            split_result = request_api(title)
            splitted_title.write(id + ',' + split_result + '\n')
        except :
            traceback.print_exc()
            continue