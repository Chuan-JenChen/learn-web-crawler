#!/usr/bin/env python
# coding: utf-8

# In[22]:


import requests as req

# 操作 browser 的 API
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 自動下載chrome，並且判斷瀏覽器版本
from webdriver_manager.chrome import ChromeDriverManager

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 強制等待 (執行期間休息一下)
from time import sleep

# 整理 json 使用的工具
import json

# 執行 command 的時候用的
import os

# 子處理程序，用來取代 os.system 的功能
import subprocess

import numpy as np

# 建立儲存json檔的資料夾
folderPath = 'youbike_in_time'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 放置爬取的資料
listData = []


# In[23]:


# 輸入爬蟲日期或時間設為檔名
def inputTime():
    text = input("input date/time: ")
    return text # 存成 json 檔的時候會用到，所以要給回傳值


# In[24]:


# 走訪頁面
def visit():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    r = req.get(url)
    obj = json.loads(r.text) # 將 json 檔變成文字檔
#     print(obj[1])
#     listData.append(obj) # 原本的寫法
    for n in range(0,1113): # 用迴圈一個一個加入是因為這樣才不會多了 json 檔原始有的中括號
        listData.append(obj[n]) # 為了要呈現 Dataframe, 導入的 json 檔中只能有一層中括號，否則還要一個一個刪
    sleep(3)
    
# 顯示每次爬的時間點
def showTime():
    print(listData[count]['sna'],listData[count]['updateTime'])


# In[19]:


# url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
# r = req.get(url)
# obj = json.loads(r.text) # 將 json 檔變成文字檔
#     print(obj[1])
#     listData.append(obj) # 原本的寫法
# for n in range(0,1113): # 用迴圈一個一個加入是因為這樣才不會多了 json 檔原始有的中括號
#     listData.append(obj[n]) # 為了要呈現 Dataframe, 導入的 json 檔中只能有一層中括號，否則還要一個一個刪
# sleep(3)
# print(listData[0]['sna'],listData[0]['updateTime'])


# In[25]:


# 存成 json 
def savejson():
    with open (f"{folderPath}/youbike_in_time_{text}.json", "w", encoding = "utf-8") as file:
        file.write(json.dumps(listData, ensure_ascii = False, indent = 4))


# ## *** 在 Anaconda prompt 輸入: jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10，會開啟 jupyter 網頁才不會報錯!!! ***

# In[ ]:


if __name__ == '__main__':
    text = inputTime() # 將回傳值丟給 text 全域變數，savejson()才能夠使用
    count = 0 # 計數器，才能讓每次
    while True:
        visit()
        showTime()
        savejson()
        sleep(180)
        count += 1113


# In[1]:


import pandas as pd
yb = pd.read_json("./youbike_in_time/youbike_in_time_0715.json", orient = 'columns')
# yb.loc[:10,['sno','sna','tot','bemp','sbi','lat','lng','srcUpdateTime','infoTime']]
# yb.loc[:5,['sna','tot']]
yb.loc[(yb['sno']==500101001),['sno','sna','tot','bemp','sbi','lat','lng','srcUpdateTime','infoTime']] # 顯示每次擷取所有相同站點的資訊

