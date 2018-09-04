from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re
from random import randint
from time import sleep
def openweb(link):
    #link = 'https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/6974/Italy-Serie-A'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,"permissions.default.stylesheet":2,"javascript.enabled":False,"profile.default_content_setting_values.notifications":1}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(link)
    sleep(3)
    driver.find_element_by_xpath("//button[2]").click()
    return driver

def yearlink(link):
    driver = openweb(link)
    linkl = []
    year = driver.find_elements_by_xpath('//*[@id="seasons"]/option')
    for i in year:
        l =  i.get_attribute('value')
        year = i.text
        if year in ylist:
            fulllink = 'https://www.whoscored.com'+l
            #linkl.append(fulllink)
            print(fulllink)
        else:
            pass
    driver.quit()
    #return linkl

link = 'https://www.whoscored.com'
ylist = ['2017/2018', '2016/2017', '2015/2016', '2014/2015', '2013/2014', '2012/2013', '2011/2012', '2010/2011']

clublist = ['/Regions/252/Tournaments/2/England-Premier-League','/Regions/108/Tournaments/5/Italy-Serie-A','/Regions/206/Tournaments/4/Spain-La-Liga','/Regions/81/Tournaments/3/Germany-Bundesliga','/Regions/74/Tournaments/22/France-Ligue-1']


for i in clublist:
    clublink = link+i
    yearlink(clublink)


