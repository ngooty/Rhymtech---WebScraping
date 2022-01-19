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
from iteration_utilities import unique_everseen,duplicates


# In[2]:


input_list=[{'name': 'Lodash', 'version': '4.17.15', 'url': 'http://www.nichemedia.io'},
 {'name': 'WordPress', 'version': '5.5.3', 'url': 'http://www.rhymtech.com'},
 {'name': 'jQuery', 'version': '1.12.4', 'url': 'http://www.rhymtech.com'},
 {'name': 'Modernizr', 'version': '2.8.3', 'url': 'http://www.rhymtech.com'},
 {'name': 'jQuery Migrate',
  'version': '1.4.1',
  'url': 'http://www.seprod.com'},
 {'name': 'jQuery', 'version': '1.12.4', 'url': 'http://www.seprod.com'},
 {'name': 'jQuery', 'version': '1.12.4', 'url': 'http://www.basf.com'},
 {'name': 'Moment.js', 'version': '2.24.0', 'url': 'http://www.infineon.com'},
 {'name': 'Snap.svg', 'version': '0.5.1', 'url': 'http://www.infineon.com'},
 {'name': 'jQuery', 'version': '3.5.1', 'url': 'http://www.infineon.com'},
 {'name': 'Modernizr', 'version': '3.3.1', 'url': 'http://www.infineon.com'},
 {'name': 'jQuery UI', 'version': '1.12.1', 'url': 'http://www.kuk-is.de'},
 {'name': 'jQuery', 'version': '1.12.4', 'url': 'http://www.kuk-is.de'}]


# In[3]:


product_list=[]
url_list=[]
for input in input_list:
    name=input['name'].lower()
    version=input['version']
    input_url=input['url']
    temp=name +' '+ version
    product_list.append(temp)
    url_list.append(input_url)


# In[4]:


#create a duplicate url list

dup_url_list=list(unique_everseen(duplicates(url_list)))


# In[5]:


url = 'https://cvedetails.com'
title='Wappalyzer'
day = date.today()


# In[6]:


dynamic_list = []
with open('Dynamic Alerts-11-01-2021.csv',encoding='latin1') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader,None) ### Skip the header 
        for row in csv_reader:
            dynamic_list.append(row)
directory = title+'_'+str(day)
pth =  os.path.join(os.getcwd(),directory)


# In[7]:


options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(chrome_options=options)
#browser=webdriver.Chrome()


# In[8]:


def main_function(df,vulnerability_url,entry_flag):
#toCSV
    def generateCSV(url_data,file_name,header_list,tool_list):
        mode='a'
        flag=False
 
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
    
    zday = str(date.today())
    calendar.month_abbr[day.month]
    month_name = calendar.month_abbr[day.month]
    current_time = time.strftime("%H:%M:%S")
    file_name=""
    brand_data=[]
    flag=False
    prev_url=""
    header_list = ['alert','category','evidence','cve','alert_score','alert_severity','location_of_vulnerability','impact','remediations_and_recommendations','time_stamp','time']
    #based on value get all other fields from dynamic alert sheet

    #Check if url has already been updated in the csv file for atleast one vulnerability

    for element in dynamic_list:
        if len(df)!=0:
            df.sort_values(by='CVE ID',ascending=False)
            if "Outdated Softwares Detected" in str(element) and not flag:
                brand_data.append([element[1],element[2],df['CVE ID'][0],df['Score'][0],element[5],element[6],vulnerability_url,element[3],element[4],month_name,zday])
                file_name = element[7].strip()
                category = element[2]
                flag=True
        else:
            if "Outdated Softwares not Detected" in str(element) and not flag and not entry_flag:
                #print('inside else')
                brand_data.append([element[1],element[2],'-',"-",element[5],element[6],vulnerability_url,element[3],element[4],month_name,zday])
                file_name = element[7].strip()
                category = element[2]
                flag=True
    
    #generate csv with given header list and alerts 
    if flag:
        generateCSV(title,file_name,header_list,brand_data)
    trust_time_out = datetime.now().time().strftime('%H:%M:%S')


# ### Main Program

# In[ ]:


entry_flag=True
entered_url=[]
header_list=['#','CVE ID','CWE ID','# of Exploits','Vulnerability Type(s)','Publish Date','Update Date','Score','Gained Access Level','Access','Complexity','Authentication','Conf.','Integ.','Avail.']
df=pd.DataFrame(columns=header_list)
for counter,product in enumerate(product_list):
    browser.get(url)
    u = browser.find_element_by_xpath('//input[@id="unifiedsearchinput"]')
    u.send_keys(product)
    u.send_keys(Keys.RETURN) 
    
    jscode='''
    var allButtons=document.getElementsByClassName('gs-title');
    for( b of allButtons){
       b.click();
     }
    '''
    browser.execute_script(jscode)
    search_string=product.split(' ')[1] +' : Security vulnerabilities'
    #get current window handle
    current_window = browser.current_window_handle
#get first child window
    for j in reversed(range(len(browser.window_handles))):
        chwd = browser.window_handles[j]
        browser.switch_to.window(chwd)
        result=browser.page_source
        browser.get(browser.current_url)
        p = re.compile(r'\b%s\b' %search_string)
#Check if the version exactly matches in the results pages. if exact match found proceed 
        if p.search(result) is None:
            entry_flag=False
            if j!=0:
                browser.close()
        else:
            result_pages=browser.find_element_by_xpath('//*[@id="vulnslisttable"]')
            entry_flag=True
            #result_link=result_pages.find_elements_by_xpath('.//a')[0].get_attribute('href')
            #browser.get(result_link)
            rows=result_pages.find_elements_by_xpath('.//tr[@class="srrowns"]/td')
            
            row_count=int(len(rows)/15) # Each row contains 15 columns in the site. 
            k=0
            col=[]
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
            print('before writing to file with vulnerabilities: ',str(url_list[counter]))
            main_function(df,url_list[counter],entry_flag)
            df = df[0:0]
            entered_url.append(url_list[counter])
            break
    if not url_list[counter] in dup_url_list and not entry_flag:  
        main_function(df,url_list[counter],entry_flag)
        entered_url.append(url_list[counter])

for dup_url in dup_url_list:
    if not dup_url in entered_url:
        entry_flag=False
        main_function(df,dup_url,entry_flag)
   


# In[ ]:




