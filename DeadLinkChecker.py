#!/usr/bin/env python
# coding: utf-8

# ## 20th Jan 2021

# In[1]:


import requests
from bs4 import BeautifulSoup
import os
import sys
import time as t
from datetime import datetime,date
from iocparser import IOCParser
from configparser import RawConfigParser
from urllib.parse import urljoin, urlparse,quote
from urllib.request import urlopen
from urllib import request
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.options import DesiredCapabilities
from icecream import ic
import cv2
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import plotly
from bs4 import BeautifulSoup,SoupStrainer
from iso3166 import countries
from requestium import Session
from PIL import Image
import csv
import json as JSON
import socket
import calendar
from operator import itemgetter
import pytesseract
import base64


# In[2]:


domain='rhymtech.com'
url = 'https://www.deadlinkchecker.com/'


# In[3]:


#options = FirefoxOptions()
#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True

options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options)

#browser=webdriver.Firefox(options=options,executable_path='/usr/local/bin/geckodriver',capabilities=firefox_capabilities)


# In[4]:



try:
    #browser.execute_script("window.location.href='"+login_url+"'")
    browser.get(url)
    u = browser.find_element_by_xpath('//input[@id="url"][@type="text"]')
    u.send_keys(domain)
    u.send_keys(Keys.RETURN) 
    
    t.sleep(5)
except Exception as e:
    print(str(e))


# In[5]:


def get_captcha_text():
    img_base64 = browser.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, browser.find_element_by_xpath('//*[@id="captcha"]'))
    with open(r"image.jpg", 'wb') as f:
        f.write(base64.b64decode(img_base64))
    captcha_text=pytesseract.image_to_string('image.jpg',config='--psm 6').split('\n')[0].replace(" ","")
    return captcha_text

def enter_captcha():
# get text from html tag
    try:
        browser.implicitly_wait(10)
        captchatextbox=browser.find_element_by_xpath('//input[@id="captchatxt"]')
        if not captchatextbox.text:
            captchatextbox.clear()
        captcha_text = get_captcha_text()
    except:
        captcha_text = get_captcha_text()
    WebDriverWait(browser, 20).until(EC.visibility_of(captchatextbox))
    captchatextbox.send_keys(captcha_text)
    WebDriverWait(browser, 20).until(EC.visibility_of(captchatextbox))
    captchatextbox.send_keys(Keys.RETURN)
    return


# In[6]:


i=0
enter_captcha()

while i<10:
    try:
        WebDriverWait(browser, 3).until(EC.invisibility_of_element((By.XPATH,'//input[@id="captchatxt"]')))
    #browser.find_element_by_xpath('//input[@id="captchatxt"]')
        i=100
    except:
        enter_captcha()
    i+=1

while True:
    try:
        progress=browser.find_element_by_xpath('//*[@id="progress"]')
    except:
        browser.implicitly_wait(20)
    if progress.get_attribute('class')!="progressstop":
        browser.implicitly_wait(60)
    else:
        break


# In[7]:


dead_links=[]
#for i in range(max_pages):
result_pages=browser.find_elements_by_xpath('//td[@style="color: rgb(176, 0, 0);"]')
no_of_result_pages=len(result_pages)
i=1
while i<=no_of_result_pages:
        #dead_links.append(browser.find_element_by_xpath(".//p[@id='"+id+"']").text)
        dead_links.append(result_pages[i].text)
        i+=3


# In[8]:


s=browser.title
title=s.strip().split('-')[1]
title=title.strip()


# ### Extract the negative sentiment text for the brand

# In[9]:



#alerts_list
dynamic_list = []
with open('Dynamic Alerts-11-01-2021.csv',encoding='latin1') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader,None) ### Skip the header 
    for row in csv_reader:
        dynamic_list.append(row)

#toCSV
def generateCSV(url_data,file_name,header_list,tool_list):
    mode='a'
    flag=False
    directory = str(url_data).strip()+'_'+str(day)
    pth =  os.path.join(os.getcwd(),directory)
 
    if os.path.exists(pth):
        pass
    else:
        os.mkdir(pth) 
    os.chdir(pth)
    if not os.path.exists(file_name):
        mode='w'
        flag=True
    with open(os.path.join(pth,file_name),mode) as f:
        csv_writer = csv.writer(f)
        if flag:
            csv_writer.writerow(header_list)
            flag=False
        if any(isinstance(i, list) for i in tool_list):
            #print(tool_list)
            csv_writer.writerows(tool_list)
            
        else:
            #print(tool_list)
            csv_writer.writerow(tool_list)

#time and month
time = datetime.now()
day = date.today()
zday = str(date.today())
calendar.month_abbr[day.month]
month_name = calendar.month_abbr[day.month]
current_time = time.strftime("%H:%M:%S")
file_name=""
brand_data=[]
flag=False
header_list = ['alert','category','domain','evidence','impact','remediations_and_recommendations',
               'alert_score','alert_severity','time_stamp','time']
    #based on value get all other fields from dynamic alert sheet

for element in dynamic_list:
    if len(dead_links)!=0:
         if "Broken Links Found" in str(element) and not flag:
            brand_data.append([element[1],element[2],domain,str(dead_links),element[3],element[4],element[5],element[6],month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    else:
        if "No Broken Links" in str(element) and not flag:
            #print('inside else')
            brand_data.append([element[1],element[2],'-',"-",'-','-',"-","-",month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    
    #generate csv with given header list and alerts 
if flag:
    generateCSV(title,file_name,header_list,brand_data)
trust_time_out = datetime.now().time().strftime('%H:%M:%S')
#trust_used_time = (datetime.strptime(trust_time_out,'%H:%M:%S') - datetime.strptime(trust_time_in,'%H:%M:%S'))


# In[ ]:





# In[ ]:




