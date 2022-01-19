#!/usr/bin/env python
# coding: utf-8

# ## 14th Jan 2021

# In[ ]:


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


# In[ ]:


username = 'ngooty@gmail.com'
passwd = 'Nagraj7*'
domain='amazon.com'
login_url = 'https://app.brand24.com/user/login/'
project_url='https://app.brand24.com/projects/new/general/phrases'
service_url=""


# In[ ]:


#options = FirefoxOptions()
#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True

options=Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options)
#browser=webdriver.Firefox(options=options,executable_path='/usr/local/bin/geckodriver',capabilities=firefox_capabilities)


# In[ ]:


def enter_domain_details(webbrowser,project_url):
        webbrowser.get(project_url)
        #webbrowser.execute_script("window.location.href='"+project_url+"'")
    #try:
        webbrowser.find_elements_by_xpath("//span[contains(text(), 'Enter Keywords')]")
        #editor = WebDriverWait(webbrowser, 20).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text"][@tabindex="0"]')))
        #editor = WebDriverWait(webbrowser, 20).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="react-select-2-input"][@type="text"][@tabindex="0"]')))
        domain_name=webbrowser.find_element_by_xpath('//input[@id="react-select-2-input"][@type="text"][@tabindex="0"]')
        domain_name.send_keys(domain)
        webbrowser.find_element_by_xpath("//button[@class='button-2mD3PwT9 button--cta-2MWn4zUq']").click()
        t.sleep(5)
        dropdown=webbrowser.find_element_by_xpath("//div[@class='css-1bcrlj0-singleValue']")
        dropdown_select= WebDriverWait(webbrowser, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text"][@tabindex="0"]')))
        dropdown_select.send_keys('English')
        webbrowser.find_element_by_xpath("//button[@class='button-2mD3PwT9 button--cta-2MWn4zUq gtm_event']").click()
        t.sleep(5)
        #print(webbrowser.current_url)
        service_url=webbrowser.current_url
        sid=service_url.split('/')[-1]
    #except Exception as e:
        #print('Error in "enter_domain_details" function. "Please check...!')
        
        #print(webbrowser.current_url)
        return webbrowser.current_url


# In[ ]:



try:
    #browser.execute_script("window.location.href='"+login_url+"'")
    browser.get(login_url)
    u = browser.find_element_by_name('login')
    u.send_keys(username)
    p = browser.find_element_by_name('password')
    p.send_keys(passwd)
    p.send_keys(Keys.RETURN)
    project_url='https://app.brand24.com/panel/'
    browser.get(project_url)
except Exception as e:
    print(str(e))


# In[ ]:


if domain in browser.page_source:
    try:
        print(browser.current_url)
        service_url=browser.find_element_by_xpath("//a[@title='"+domain+"']").get_attribute("href")
    except:
        project_url='https://app.brand24.com/projects/new/general/phrases'
        service_url=enter_domain_details(browser,project_url)
else:
    project_url='https://app.brand24.com/projects/new/general/phrases'
    service_url=enter_domain_details(browser,project_url)
    


# In[ ]:


if len(service_url)!=0:   
    browser.get(service_url)
    #browser.execute_script("window.location.href='"+service_url+"'")
    t.sleep(10)

#Click the check boxes 'forums' and 'blogs' in the page
    #try:
    radio_button1=browser.find_element_by_xpath("//input[@id='selected_category_3']")
    browser.execute_script("arguments[0].click();", radio_button1)
    radio_button2=browser.find_element_by_xpath("//input[@id='selected_category_6']")
    browser.execute_script("arguments[0].click();", radio_button2)
    #WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.NAME, 'selected_category_6'))).click()
    #WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, 'selected_category_3'))).click()
    #except Exception as e:
    t.sleep(10)
    browser.get(browser.current_url)
    t.sleep(30)
else:
    print('service_url string is empty. Please check...!')
    exit()


# In[ ]:


comments=[]
inc=1
#for i in range(max_pages):
result_pages=browser.find_elements_by_xpath('//*[@id="results_content"]/div[1]/div[5]/a')
no_of_result_pages=len(result_pages)

while (no_of_result_pages)>1:
    negative_comments=browser.find_elements_by_xpath(".//select[@class='sentiment negative']")
    for element in negative_comments:
        id='mention_text_'+str(element.get_attribute('id').split('-')[2])
        comments.append(browser.find_element_by_xpath(".//p[@id='"+id+"']").text)
        
    try:       
        if len(result_pages)==2:
            link=browser.find_element_by_xpath('//*[@id="results_content"]/div[1]/div[5]/a[4]')
            browser.execute_script("arguments[0].click();", link)
        else:
            link=browser.find_element_by_xpath('//*[@id="results_content"]/div[1]/div[5]/a[5]')
            browser.execute_script("arguments[0].click();", link)
        no_of_result_pages-=1
        t.sleep(10)
    except Exception as e:
        print('inside exception '+ str(e))
        t.sleep(10)
        break


# In[ ]:


s=browser.title
url_data=s.strip().split('-')[1]
url_data=url_data.strip()


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
    directory = str(url_data)+'_'+str(day)
    path =  os.path.join(os.getcwd(),directory)
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path) 
    if not os.path.exists(file_name):
        mode='w'
        flag=True
    with open(os.path.join(path,file_name),mode) as f:
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
header_list = ['alert','category','domain','date','score','cause','evidence','impact','remediations_and_recommendations','alert_score','alert_severity','time_stamp','time']
    #based on value get all other fields from dynamic alert sheet

for element in dynamic_list:
    if len(comments)!=0:
        if "Negative Discusion Found" in str(element) and not flag:
            brand_data.append([element[1],element[2],url_data,zday,element[5],'-',str(comments),element[3],"Review/Analyze them",element[5],element[6],month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    else:
        if "No Negative Discusion" in str(element) and not flag:
            #print('inside else')
            brand_data.append([element[1],element[2],url_data,zday,'-',"-",'-',element[3],"-","-","-",month_name,zday])
            file_name = element[7].strip()
            category = element[2]
            flag=True
    
    #generate csv with given header list and alerts 
if flag:
    generateCSV(url_data,file_name,header_list,brand_data)
trust_time_out = datetime.now().time().strftime('%H:%M:%S')
#trust_used_time = (datetime.strptime(trust_time_out,'%H:%M:%S') - datetime.strptime(trust_time_in,'%H:%M:%S'))


# In[ ]:





# In[ ]:




