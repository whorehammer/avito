#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests, bs4, os, random, pytesseract, json, base64, os, time
from PIL import Image
from datetime import datetime, timedelta
import os.path
import re
s = requests.Session()

proxy = "http://aviparser.zzz.com.ua/prox.php?page="
links = ["https://www.avito.ru/rossiya/lichnye_veschi"]
for link in links:
    for i in range(200):
        url = link + "?p=" + str(i+1)
        print("page " + str(i+1))
        time.sleep(5)
        while True:
            try:
                content = s.get(proxy + url)
                if len(content.history) > 0:
                    if content.history[0].status_code == 301:
                        exit("total pages %s" % str(i))
                break
            except:
                time.sleep(10)
        parser = bs4.BeautifulSoup(content.text, "html.parser")
        obs = parser.findAll("a", {"class":"item-description-title-link"})
        for ob in obs:
            href= 'https://www.avito.ru' + ob.attrs['href']
            print(href)
            #page = s.get(href)
            #page_parser = bs4.BeautifulSoup(page.text, "html.parser") #seller-info-name js-seller-info-name
            time.sleep(10)
            while True:
                try:
                    resp = requests.get(proxy + href)
                    break
                except:
                    time.sleep(10)
            parser = bs4.BeautifulSoup(resp.text, "html.parser")
            script = parser.find("script", text=lambda text: text and "avito.item.id" in text)
            try:
                code = script.text
            except:
                continue
            vars = code.split(';')
            item_id = ''
            item_phone = ''
            for var in vars:
               if('avito.item.phone' in var):
                  item_phone = var.split('=')[1].replace("'", "").replace(" ", "")
               elif('avito.item.id' in var):
                  item_id = var.split('=')[1].replace("'", "").replace(" ", "")
            
            
            url1= "http://aviparser.zzz.com.ua/head_send.php?item_id={0}&item_phone={1}&link={2}".format(item_id, item_phone, link)
            pkey = requests.get(url1)
            pkey = pkey.text
            try:
              img = json.loads(pkey)
            except Exception as e:
              print(e)
              continue
            try:
                imgdata = base64.b64decode(img["image64"].replace("data:image/png;base64,", ""))
            except:
                print(img)
                continue
            filename = 'aaa.png'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            img = Image.open('aaa.png')
            phone = pytesseract.image_to_string(img)
            os.remove('aaa.png')
            name_div = parser.findAll("div", {"class": "seller-info-name"})[0]
            name = name_div.find('a')
            if(name != None and len(name) > 0):
              name = name.text.strip()
              if(len(name.split()) == 2 or len(name.split()) == 3):
                 try:
                     assert all(all(re.search("[а-яА-Я]", a) is not None for a in n) is True for n in name.split())
                     assert all(a[0].isupper() for a in name.split())
                 except AssertionError:
                     print(name)
                     continue
                 print("found " + name)
                 date = parser.find("div", {"class":"title-info-metadata-item-redesign"})
                 title = parser.find("span", {"class": "title-info-title-text"})
                 try:
                     date = date.text
                     if 'сегодня' in date:
                         date = datetime.today().strftime('%Y-%m-%d')
                     elif 'вчера' in date:
                         date = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")
                     title = title.text
                 except Exception as e: 
                     print(e)
                     print("wrong data")
                     continue
                 print(name, date, title)
                 requests.get("http://aviparser.zzz.com.ua/writer.php?title={0}&date={1}&name={2}&phone={3}&href={4}".format(title, date, name, phone, href))
                 

            

            

            
            
