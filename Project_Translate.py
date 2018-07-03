
# coding: utf-8

# In[46]:


import os
import sys
import urllib.request
import json
client_id = "U3jYajT3oAEeQR2X7idf"
client_secret = "GA9o1AmeqS"
def hanrom(text) :
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/krdict/romanization?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return(json.loads(response_body.decode('utf-8'))['aResult'][0]['aItems'][0]['name'])
    else:
        return("Error Code:" + rescode)

