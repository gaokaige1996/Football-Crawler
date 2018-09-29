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

def obtaintable(link):
    driver = openweb(link)
    l = []
    table = driver.find_element_by_xpath('//tbody[@class="standings"]')
    team = table.find_elements_by_xpath("//tbody[@class='standings']/tr")
    #'//span/input[@class='s_ipt']'
    for i in team:
        teamname = i.text
        l.append(teamname)
    driver.quit()
    return l

#link = 'https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/6829/England-Premier-League'

ylist = ['2017_2018', '2016_2017', '2015_2016', '2014_2015', '2013_2014', '2012_2013', '2011_2012', '2010_2011']
namelist = ['England-Premier-League','Italy-Serie-A','Spain-La-Liga','Germany-Bundesliga','France-Ligue-1']

file = open("yearlinkl.txt")

txtnamel = []
for i in namelist:
    for y in ylist:
        txtname = i+'_'+y+'.txt'
        txtnamel.append(txtname)

m = 0
for line in file.readlines():
    line = line.strip('\n')
    with open(txtnamel[m],'w') as f:
        print(txtnamel[m])
        table = obtaintable(line)
        for i in table:
            f.write(i + '\n')
            print(i)
    m = m + 1
