#!/usr/bin/env python
# coding: utf-8

# ### Web Scraping - scamadviser.com

# In[1]:


import pandas as pd
import numpy as np
import re
import os
import getopt, sys
import requests
import urllib.request
from os import path
from urllib.request import Request, urlopen


# In[2]:


argumentlist = sys.argv[1:]
options="huf:"
long_opts=['Help','url','urlfile']


# In[17]:


def display_usage():
    print()
    print("Usage: ")
    print()
    print("python "+sys.argv[0]+" -[huf] url [--[Help,url,urlfile]]")
    print() 
    print("For single url:")
    print()
    print("Eg: "+"python "+sys.argv[0]+" -u example.com")
    print("Eg: "+"python "+sys.argv[0]+" --url example.com")
    print()
    print("For more than one url, write all the urls in a separate line and provide the file name")
    print() 
    print("Eg: "+"python "+sys.argv[0]+" -f urlfile_name")
    print("Eg: "+"python "+sys.argv[0]+" --urlfile urlfile_name")
    print()
    sys.exit()


# In[4]:


urlfile=""
single_url=""
if len(sys.argv)<3:
    display_usage()
else:
    try:
        arguments, values = getopt.getopt(argumentlist, options, long_opts)
    # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
            #print ("Diplaying Help")
                display_usage()
            elif currentArgument in ("-f", "--urlfile"):
                urlfile=sys.argv[2]
             
            elif currentArgument in ("-u", "--url"):
                single_url=sys.argv[2]
             
    except getopt.error as err:
    # output error, and return with an error code
        print (str(err))


# In[5]:


master_file=pd.read_excel('Scam Adviser score sheet.xlsx')
dynamic_file=pd.read_excel('scam adviser dynamic alerts.xlsx')


# In[6]:


merged_df=pd.merge(master_file,dynamic_file,how='outer',right_on='VULNERABILITY NAME',left_on='Alert name')


# ### Impute null values with most frequent values from the master sheet. 

# In[7]:


null_cols=merged_df.columns[merged_df.isna().any()].tolist()

for col in null_cols:
    merged_df[col].fillna(merged_df[col].mode,inplace=True)


# In[8]:


master_trust_score=[]
for score in merged_df['Checklist'].to_string().splitlines():
    master_trust_score.append(score.split('Score',1)[1].replace('(',"").replace(')',""))
    #print(score.split('Score',1)[1].replace('(',"").replace(')',""))


# In[9]:


high_range=[]
for score in master_trust_score:
    if "-" in score:
        #user=score[score.find("-")+0:].splitlines()
        high_range.append(int(score.split('-')[1]))
    elif "<" in score:
        high_range.append(int(score.split('<')[1]))
    else:
        high_range.append(int(score))               

range_values={i: high_range[i] for i in range(0, len(high_range), 1)}


# In[10]:


#url="hdfcbank.com"


# ### Trying out scrapingbee.com. This site is similar to scraping ant with one month free subscription and allows 1000 requests3

# In[11]:


import requests

def get_trust_score(url):
    ind=np.nan
    trust_score=""
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": "GYISVV3BEGZF79FM2UW9X20KQUVYZG11I5WO1MR3SVWWPCP6IH4QC69ZPSZQ7HY5H9MNQ12TF0DJ0RHS",
            "url": "https://www.scamadviser.com/check-website/"+url,  
        },
        
    )
    #print('Response HTTP Status Code: ', response.status_code)
    if response.status_code!=200:
        print('url '+url+' is not reachable. Please check...!')
    else:
        data=response.content
        data=data.decode("utf-8")
        
        for line in data.split():
            if "data-percentage" in line:
                trust_score=''.join(c for c in line if c in '0123456789')
 
    try:
        for key,val in range_values.items():
            if int(trust_score)<=val:
                ind=key
    except:
        print('Scraping of '+url+ ' is not done correctly. Rerun the scraping script')
    return trust_score,ind


# In[12]:


# We have to chop off "http://", "https://" and "www." in the url. scamadviser.com takes only sitename (example.com)
def edit_url(url):
    if "https" in url:
        url=re.sub('https://','',url)
    if "http" in url:
        url=re.sub('http://','',url)
    if "www" in url:
        url=re.sub('www.','',url)
    return url


# In[13]:


def write_to_csv(observed_score,index):
    file='observed_trust_score.csv'
    export_df=merged_df.iloc[[index],[1,3,5,6,7,8,12,13,14]]
    export_df['Observed URL']=url
    export_df['Observed Trust Score']=observed_score
    if not index:
        export_df['Comments']='Success'
    else:
        export_df['Comments']='Failed. Try again'
    #write the trust score and other details into a csv file
    if not path.exists(file):
        export_df.to_csv(file)
    else:
        export_df.to_csv(file, mode='a', header=False)


# In[14]:


urlfile='urlfile.txt'


# In[15]:


if single_url:
    url=edit_url(single_url)
    trust_score,row_index=get_trust_score(url)
    write_to_csv(trust_score,row_index)
elif not path.exists(urlfile):
    print('Incorrect url file passed as an argument. Please check...!')
    exit
else:
    with open(urlfile,'r') as f:
        lines=f.readlines()
        for line in lines:
            url=line
            if url.startswith('#'):
                pass
            else:
                url=edit_url(url)
                trust_score,row_index=get_trust_score(url)
                write_to_csv(trust_score,row_index)

                #print('final else loop')


# In[16]:



#new_row=merged_df.iloc[row_index][['Alert name','Impact','alert score','alert severity','dimension','Sub Dimension','Checklist','Observation','RHYM Score']]


# In[ ]:




