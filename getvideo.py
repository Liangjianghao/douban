#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/4 13:56
# @Author : LiangJiangHao
# @Software: PyCharm

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 22:38
# @Author : LiangJiangHao
# @Software: PyCharm

import os
import sys
import requests
import re
from lxml import html
from selenium import webdriver
import time
import json
import urllib
import pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def getUpTime(url):
    response = requests.get(url, verify=False).content
    selector = html.fromstring(response)
    productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"首播")]/following-sibling::*/text()')
    if len(productInfo) == 0:
        productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"上映日期")]/following-sibling::*/text()')
    if '(' in productInfo[0]:
        uptime = productInfo[0].split('(')[0]
    else:
        uptime = productInfo[0]
    if len(uptime) == 4:
        uptime = '%s-1-1' % uptime
    # print(uptime)
    return uptime


client = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='douban',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cur = client.cursor()

baseUrl = 'https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=喜剧,2018'
baseUrl='https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=2018,动漫'
baseUrl='https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=2018,电影,喜剧'
baseUrl='https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=电影,中国大陆,2018'
baseUrl='https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=纪录片'
baseUrl='https://movie.douban.com/tag/#/?sort=S&range=0,10&tags=电影,2018'
# baseUrl='https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=喜剧,2018,中国大陆,电影,青春'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
driver = webdriver.Firefox()
driver.get(baseUrl)
response = driver.page_source
selector = html.fromstring(response)

for x in range(1,1000):
    print('正在抓取第%s页数据'%(x+1))
    try:
        nextPage = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/a')
        nextPage.click()
        time.sleep(3)
    except Exception as e:
        print(e)
        break
response = driver.page_source
selector = html.fromstring(response)
movieArr=selector.xpath('//*[@id="app"]/div/div[1]/div[3]/a')
print(len(movieArr))
videoNumber=len(movieArr)
def eleIsTrue(ele,xpathStr):
    try:
        theEle=ele.xpath(xpathStr)[0]
        # print(theEle)
        return True
    except Exception as e:
        return False
for index,movie in enumerate(movieArr):
    try:
        print('正在解析第%s/%s个电影'%(index+1,videoNumber))
        url=movie.xpath('@href')[0]
        movie_id=(url.split('subject')[1]).split('/')[1]
        imgUrl=movie.xpath('div/span/img/@src')[0]
        title=movie.xpath('p/span[1]/text()')[0]
        rateStr='p/span[2]/text()'
        # if eleIsTrue(movie,rateStr):
        #     rate=movie.xpath(rateStr)[0]
        # else:
        #     rate=0
        rate = movie.xpath(rateStr)[0]
        time.sleep(1)
        uploadTime=getUpTime(url)
        insertStr = "insert into DB_All_2018 (title,movie_id,rate,url,cover,uploadTime) values ('%s','%s', '%s','%s','%s','%s')" % (title,movie_id,rate,url,imgUrl,uploadTime)
        print(insertStr)
        cur.execute(insertStr)
        client.commit()
    except Exception as e:
        print(e)
        continue


# CREATE TABLE `DB_xiju` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣喜剧';

# CREATE TABLE `DB_xiju_movie` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣喜剧电影';

# CREATE TABLE `DB_cn_2018` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣2018中国电影';

# CREATE TABLE `DB_record` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣纪录片';

# CREATE TABLE `DB_All_2018` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣2018电影';