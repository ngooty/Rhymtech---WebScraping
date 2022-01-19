#!/usr/bin/env python
# coding: utf-8

# ## 18th Jan 2021

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
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options


import matplotlib.pyplot as plt
import pandas as pd
import plotly
from bs4 import BeautifulSoup,SoupStrainer
from iso3166 import countries
from requestium import Session
from wordcloud import WordCloud, STOPWORDS
import csv
import json as JSON
import socket
import calendar
from icecream import ic


# In[2]:


username = 'ngooty@gmail.com'
passwd = 'Nagraj7*'
domain='https://yahoo.com'
url = 'https://duplichecker.com'

if not url.startswith('http'):
    url='http://'+url
if not domain.startswith('http'):
    domain='http://'+domain


# In[4]:


from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.set_preference('useHeadless', True)
profile.update_preferences()
options = Options()
options.add_argument("--headless")
desired = DesiredCapabilities.FIREFOX

browser = webdriver.Firefox(firefox_profile=profile, capabilities=desired,firefox_options=options)


# In[5]:


def switch_frame(driver,css):
    try:
        captcha_box=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,css)))
    except:
        driver.switch_to.default_content()


# In[6]:


browser.get(url)
element = browser.find_element_by_xpath('//input[@class="form-control pl_text hidden-xs check_url_c"][@type="url"]')
#element = browser.find_element_by_xpath('//input[@id="badgeUrl"][@type="text"]')
t.sleep(5)
element.send_keys(domain)
element.send_keys(Keys.RETURN)
#elem.submit()


# In[7]:


browser.implicitly_wait(30)


# In[8]:


evidence=[]
try:
    results_page=browser.find_element_by_xpath('//*[@id="ajax_container"]')
    results=results_page.find_elements_by_xpath('.//a')
    for result in results:
    #print(result.get_attribute('href'))
        if not domain in result.text:
            evidence.append(result.get_attribute('href'))
except Exception as e:
    print(str(e))
if len(evidence)==0:   
    print('No evidence of Plagiarism found for ',domain)


# In[9]:


title=browser.title.split('|')[0].strip()


# In[10]:


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
header_list = ['alert','category','evidence','alert_score','alert_severity','impact','remediations_and_recommendations','time_stamp','time']
    #based on value get all other fields from dynamic alert sheet
for element in dynamic_list:
    if len(evidence)!=0:
        if "webpage Duplications" in str(element) and not flag:
            brand_data.append([element[1],element[2],str(evidence),element[5],element[6],element[3],element[4],month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    else:
        if "No webpage Duplications Found" in str(element) and not flag:
            #print('inside else')
            brand_data.append([element[1],element[2],'-',"-",'-',"-","-",month_name,zday])
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




