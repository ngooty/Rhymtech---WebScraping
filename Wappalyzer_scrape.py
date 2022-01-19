#!/usr/bin/env python
# coding: utf-8

# ## 22nd Jan 2021

# In[1]:


import requests
from bs4 import BeautifulSoup
import os
import sys
import time as t
from datetime import datetime,date
from urllib.parse import urljoin, urlparse,quote
from urllib.request import urlopen
from urllib import request
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from icecream import ic
import cv2
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import plotly
from bs4 import BeautifulSoup,SoupStrainer
from requestium import Session
from PIL import Image
import csv
import json as JSON
import socket
import calendar
from operator import itemgetter
import pytesseract
import base64
import re
import string
import scrapy


# In[2]:


product='Weblogic Server version 9.0'
url = 'https://cvedetails.com'


# In[3]:


# Add "version" in between the product name and version number so as to make the search easy in cvedetails.com
product=product.split(' ')
version=str(product[-1])
product=str(product[0])+' version '+ version
search_in_results=product+' : Security vulnerabilities'
product


# In[4]:


#options = FirefoxOptions()
#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True

options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(chrome_options=options)


# In[5]:



#try:
    #browser.execute_script("window.location.href='"+login_url+"'")
browser.get(url)
u = browser.find_element_by_xpath('//input[@id="unifiedsearchinput"]')
u.send_keys(product)
u.send_keys(Keys.RETURN) 
    

#except Exception as e:
    #print(str(e))


# In[6]:


jscode='''
var allButtons=document.getElementsByClassName('gs-title');
for( b of allButtons){
   b.click();
 }
'''
browser.execute_script(jscode)


# In[7]:


#get current window handle
p = browser.current_window_handle

#get first child window
chwd = browser.window_handles[-1]

browser.switch_to.window(chwd)


# In[8]:


# in browser.page_source
result=browser.page_source
browser.get(browser.current_url)

p = re.compile(r'\b%s\b' %product)
ic(p.search(result))
#Check if the version exactly matches in the results pages. if exact match found proceed else exit
if p.search(result) is None:
    print('No Vulnerabilities detected for the product "',product +' "')
    print('Exiting...!')
    exit()


# In[9]:


rows=browser.find_elements_by_xpath('.//tr[@class="srrowns"]/td')
headers=browser.find_elements_by_tag_name('th')


# In[10]:


header_list=[]
for header in headers:
    header_list.append(header.text)
header_list=header_list[3:]


# In[11]:


df=pd.DataFrame(columns=header_list)
row_count=int(len(rows)/15) # Each row contains 15 columns in the site. 
k=0
col=[]
r=0
for i in range(len(rows)-1):
    for j in range(15):
        if k<len(rows):
            col.append(str(rows[k].text))
            k+=1

    if len(col)!=0:
        df.loc[len(df)]=col
        col=[] 
    else:
        break


# In[12]:


title='Wappalyzer'


# In[13]:



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
header_list = ['alert','category','evidence','cve','alert_score','alert_severity','location_of_vulnerability','impact','remediations_and_recommendations','time_stamp','time']
    #based on value get all other fields from dynamic alert sheet

for element in dynamic_list:
    if len(df)!=0:
         if "Outdated Softwares Detected" in str(element) and not flag:
            brand_data.append([element[1],element[2],df['CVE ID'],df['Score'],element[5],element[6],df['Access'],element[3],element[4],month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    else:
        if "Outdated Softwares not Detected" in str(element) and not flag:
            #print('inside else')
            brand_data.append([element[1],element[2],'-',"-",'-','-',"-","-",'-',month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    
    #generate csv with given header list and alerts 
if flag:
    generateCSV(title,file_name,header_list,brand_data)
trust_time_out = datetime.now().time().strftime('%H:%M:%S')
#trust_used_time = (datetime.strptime(trust_time_out,'%H:%M:%S') - datetime.strptime(trust_time_in,'%H:%M:%S'))


# In[ ]:




