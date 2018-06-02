#coding=utf-8
from gevent import monkey,pool
monkey.patch_socket()
import os
import gevent
from lxml import etree
import requests
import re
import pandas as pd

class Gaokao():
    def __init__(self):
        self.k=0

    def urls(self):
        #page_range=[1,23416]
        for i in range(1,1735):  #test:get all page of 2017
            print 'downloading page:>>> ',i
            url='https://data-gkcx.eol.cn/soudaxue/queryProvinceScore.html?messtype=jsonp&provinceforschool=&schooltype=&page={}&size=10&keyWord=&schoolproperty=&schoolflag=&province=&fstype=&zhaoshengpici=&fsyear=2017'.format(i)
            yield url

    def get_html(self,url):
        gevent.sleep(2)
        try:
            dic={}
            res=requests.get(url)
            res.encoding='utf-8'
            html=res.text
            res.close()
            for r in re.findall(re_,html):
                lists=[rr.encode('gb2312','ignore') for rr in r]
                dic[self.k]=lists
                self.k+=1

        #record error urls
        except:
            with open('d:\\error.txt','a') as f:
                f.write(url+'\n')
                dic[self.k]=url
        finally:
            df=pd.DataFrame.from_dict(dic,orient='index')
            df.to_csv(outputfile,mode='a',header=0,index=0)

if __name__=='__main__':
    '''
    {
    "schoolid": "38",
    "schoolname": "北京交通大学",
    "localprovince": "重庆",
    "province": "北京",
    "studenttype": "文科",
    "year": "2017",
    "batch": "本科一批",
    "var": "599",
    "var_score": "599",
    "max": "611",
    "min": "592",
    "num": "0",
    "fencha": "74",
    "provincescore": "525",
    "url": "http://gkcx.eol.cn/schoolhtm/schoolAreaPoint/38/10028/10034/10036.htm?852034"
    },
    '''
    re_=re.compile(r'"schoolname": "(.*?)",.*?"localprovince": "(.*?)",.*?"province": "(.*?)",.*?"studenttype": "(.*?)",.*?"year": "(.*?)",.*?"batch": "(.*?)",.*?"var": "(.*?)",.*?"var_score": "(.*?)",.*?"max": (.*?),.*?"min": (.*?),.*?"num": "(.*?)",.*?"fencha": "(.*?)",.*?"provincescore": "(.*?)"',re.S)
    gk=Gaokao()
    th=[]
    p=pool.Pool(30)
    outputfile='d:\\gaokao.csv'
    with gevent.Timeout(4,True) as timeout:
        for u in gk.urls():
            th.append(p.spawn(gk.get_html,u))
        gevent.joinall(th)
