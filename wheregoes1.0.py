#!/usr/bin/env python
# coding: utf-8

# ## 19th Jan 2021

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
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from icecream import ic


import matplotlib.pyplot as plt
import pandas as pd
import plotly
from bs4 import BeautifulSoup,SoupStrainer
from iso3166 import countries
from requestium import Session
from wordcloud import WordCloud, STOPWORDS
import csv
import json 
import socket
import calendar
import socket
import IP2Location


# In[2]:


domain_list=['blog.adidas-group.com', 'lyncdiscover.adidas-group.com', 'ser2009de.adidas-group.com', 'shine.adidas-group.com', 'survey.adidas-group.com', 'origin.blog.adidas-group.com', 'jobs.adidas-group.com', 'b2bportal-stg.adidas-group.com', 'report.adidas-group.com', 'herzo.adidas-group.com', 'www.herzo.adidas-group.com', 'nps-cis.adidas-group.com', 'places.adidas-group.com', 'alivevideos.adidas-group.com', 'employeecareers.adidas-group.com', 'placesws.adidas-group.com', 'staging.placesws.adidas-group.com', 'wechallenge-test.adidas-group.com', 'lyncdiscover.externals.adidas-group.com', 'b2bportal-dev.adidas-group.com', 'nps-cis-dev.adidas-group.com', 'origin.placesws.adidas-group.com', 'www.report.adidas-group.com', 'ser2009.adidas-group.com']


# In[3]:


username = 'ngooty@gmail.com'
passwd = 'Nagraj7*'
#domain='amazon.com'
url = 'wheregoes.com'
url='https://www.redirecttracker.com/'

if not url.startswith('http'):
    url='http://'+url


# In[4]:


def main_function(tracelist):
#toCSV
    def generateCSV(title,file_name,header_list,tool_list):
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
    trace_data=[]
    flag=False
    header_list = ['alert','category','domain','ip','country','evidence','impact','remediations_and_recommendations',
               'alert_score','alert_severity','time_stamp','time']
    #based on value get all other fields from dynamic alert sheet

    for element in dynamic_list:
        if len(tracelist)!=0:
            if "Redirection Found" in str(element) and not flag:
                trace_data.append([element[1],element[2],domain,ip_address,'-',tracelist,element[3],element[4],element[5],element[6],month_name,zday])
                file_name = element[7].strip()
                category = element[2]
                flag=True
        else:
            if "Redirection not Found" in str(element) and not flag:
            #print('inside else')
                trace_data.append([element[1],element[2],domain,ip_address,'-','-',"-",'-',"-",'-',month_name,zday])
                file_name = element[7].strip()
                category = element[2]
                flag=True
    
    #generate csv with given header list and alerts 
    if flag:
        generateCSV(title,file_name,header_list,trace_data)
    trust_time_out = datetime.now().time().strftime('%H:%M:%S')


# In[5]:


options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#browser = webdriver.Chrome(chrome_options=options)
browser=webdriver.Chrome()
browser.get(url)
s=browser.title
title=s.strip().split('|')[0]


# In[6]:


dynamic_list = []
day = date.today()
with open('Dynamic Alerts-11-01-2021.csv',encoding='latin1') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader,None) ### Skip the header 
        for row in csv_reader:
            dynamic_list.append(row)
directory = title+'_'+str(day)
pth =  os.path.join(os.getcwd(),directory)


# ### Main Function

# In[7]:


for domain in domain_list:
    if not domain.startswith('http'):
        https_domain='https://'+domain
    
    if domain.startswith('www'):
        get_ip=domain  
    elif not domain.startswith('http'):
        get_ip='www.'+domain
    else:
        get_ip='www.'+domain.split('/')[2]

    hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
    try:
        get_ip=get_ip.replace('www.','')
        ip_address = socket.gethostbyname(get_ip)
    except:
        ip_address='-'
    
    tracelist=[]
    #domain_name=browser.find_element_by_xpath('//input[@id="form_text"][@type="text"]')
    domain_name=browser.find_element_by_xpath('/html/body/div/div[1]/div/div/form/div[1]/div[1]/input')
    domain_name.send_keys(https_domain)
    #browser.find_element_by_xpath("//input[@id='form_button'][@type='submit']").click()
    browser.find_element_by_xpath("/html/body/div/div[1]/div/div/form/div[1]/div[2]/input").click()
    t.sleep(5)
    #parentElement = browser.find_element_by_xpath("//div[@class='tracecontent']")
    parentElement = browser.find_element_by_xpath('/html/body/div/div[1]/div/div/form')
    elementList = parentElement.find_elements_by_xpath(".//p")
    for trace in elementList:
        check_trace=trace.text
        if check_trace is not None and not domain in check_trace and check_trace!='Result of Trace':
                tracelist.append(check_trace)
    main_function(tracelist)
    browser.get(url)


# In[ ]:





# In[ ]:




