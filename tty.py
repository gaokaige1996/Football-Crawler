from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import re
from random import randint
from time import sleep
import traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def openweb(link):
    # link = 'https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/6974/Italy-Serie-A'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2, "permissions.default.stylesheet": 2,
             "javascript.enabled": False, "profile.default_content_setting_values.notifications": 1}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(link)
    #sleep(3)
    return driver

def write(l,year):
    with open('Germany'+year+'.txt','w') as f:
        for i in l[1:]:
            if i  != '':
                i = i.replace(' ','')
                i = i.replace('\n','  ')
                f.write(i+'\n')
            else:
                pass

week = '52'
yearl= ['2011']
country = '75'
for year in yearl:
    link = 'https://www.clubworldranking.com/ranking-coaches/wd/'+week+'/yr/'+year+'/nationality/'+country
    driver = openweb(link)
    m = driver.find_elements_by_xpath('//*[@id="ctl00_divLeft"]/div/div/div/div/div/div/div/div[3]/table/tbody/tr')
    table = []
    for i in m:
        row = i.text
        table.append(row)
    write(table,year)
    print('Germany',year,'has finished')
    driver.quit()
