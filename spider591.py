# -*- coding: utf-8 -*-
"""
author:Ane
"""
import sys
from bs4 import BeautifulSoup
import requests
import json
import time
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")

def dealDate(url):
   header = {
      "Host":"rent.591.com.hk",
      "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
      "Accept":"application/json, text/javascript, */*; q=0.01",
      "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding":"gzip, deflate, br",
      "Referer":"https://rent.591.com.hk/",
      "X-Requested-With":"XMLHttpRequest",
      "Cookie":"think_language=zh-hk; think_template=default; PHPSESSID=nc8mgk24fa4qo1hu4f2ut2v1l5; __asc=cefa42e715b83db8b19bd2da4b9; __auc=cefa42e715b83db8b19bd2da4b9; _ga=GA1.3.834050676.1492565855; _gat=1; _gat_rent=1",
      "Connection":"keep-alive"
   }
   web_date = requests.get(url,headers = header)
   dates = json.loads(web_date.text)

   db = MySQLdb.connect("localhost", "root", "mysqlmima", "rentdate",charset = "utf8")
   cursor = db.cursor()


   for date in dates["items"]:
      price = date["price"].strip()
      address = date["address"].strip()
      area = date["area"].strip()
      linkman = date["linkman"].strip()
      img = date["cover_img"].strip()
      print price, address, area, linkman, img

      sql = """INSERT INTO biao_rentdate (ADDRESS, AREA, LINKMAN, PRICE, IMG) VALUES ('%s', '%s', '%s', '%s', '%s')"""%(address,area,linkman,price,img)
      try:
         cursor.execute(sql)
         db.commit()
      except:
         db.rollback()

   db.close()



def start():

   urls = ['https://rent.591.com.hk/?m=home&c=search&a=rslist&v=new&type=1&hasimg=1&searchtype=1&p={0}'.format(str(i)) for i in range(1,175)]
   for url in urls:
      dealDate(url)


start()

