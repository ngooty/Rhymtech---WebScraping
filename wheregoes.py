#!/usr/bin/env python
# coding: utf-8

# ## 19th Jan 2021

# In[7]:


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
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.options import DesiredCapabilities
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


username = 'ngooty@gmail.com'
passwd = 'Nagraj7*'
domain='amazon.com'
url = 'wheregoes.com'

if not url.startswith('http'):
    url='http://'+url
if not domain.startswith('http'):
    target_url='http://'+domain
    
if domain.startswith('www'):
    get_ip=domain   
elif not domain.startswith('http'):
    get_ip='www.'+domain
else:
    get_ip='www.'+domain.split('/')[2]

hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(get_ip)


# In[3]:


#options = FirefoxOptions()
#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True

options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options)
#browser=webdriver.Firefox(options=options,executable_path='/usr/local/bin/geckodriver',capabilities=firefox_capabilities)


# In[ ]:


browser.get(url)
domain_name=browser.find_element_by_xpath('//input[@id="form_text"][@type="text"]')
domain_name.send_keys(domain)
browser.find_element_by_xpath("//input[@id='form_button'][@type='submit']").click()
t.sleep(5)


# In[ ]:


browser.current_url
tracelist=[]
#trace_results=browser.find_elements()
parentElement = browser.find_element_by_xpath("//div[@class='tracecontent']")
elementList = parentElement.find_elements_by_xpath(".//*")
for trace in elementList:
    check_trace=trace.get_attribute('href')
    if check_trace is not None and 'https://wheregoes.com/' not in check_trace:
        if not domain in check_trace: 
            tracelist.append(check_trace)


# In[ ]:


s=browser.title

url_data=s.strip().split('|')[0]


# ### Extract the negative sentiment text for the brand

# In[ ]:



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
    generateCSV(url_data,file_name,header_list,trace_data)
trust_time_out = datetime.now().time().strftime('%H:%M:%S')
#trust_used_time = (datetime.strptime(trust_time_out,'%H:%M:%S') - datetime.strptime(trust_time_in,'%H:%M:%S'))


# In[ ]:




