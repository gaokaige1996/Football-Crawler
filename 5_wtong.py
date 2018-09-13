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
    sleep(3)
    try:
        driver.find_element_by_xpath("//a[@class = 'banner_continue--2NyXA']").click()
    except:
        pass
    # driver.find_element_by_xpath("/html/body/div[9]/div[1]/div/div/div[2]/a[2]").click()
    return driver


def selectcatogory(link, category):
    driver = openweb(link)
    playerlink = driver.find_element_by_xpath('//*[@id="sub-navigation"]/ul/li[4]/a').get_attribute('href')
    driver.get(playerlink)
    # detailed = driver.find_element_by_xpath('//*[@id="detailed-statistics-tab"]/a')
    # detailed.click()
    detailed = driver.find_element_by_xpath('//*[@id="detailed-statistics-tab"]/a')
    driver.execute_script("arguments[0].click();", detailed)
    WebDriverWait(driver, 60, 0.5).until(
        EC.presence_of_element_located((By.ID, 'category')))
    s1 = Select(driver.find_element_by_id('category'))
    s1.select_by_value(category)
    sleep(5)
    return driver


def obtainplayer(driver):
    sleep(5)
    WebDriverWait(driver, 60, 0.5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="player-table-statistics-body"]/tr')))
    table = driver.find_elements_by_xpath('//*[@id="player-table-statistics-body"]/tr')
    l = []
    for i in table:
        player = i.text
        l.append(player)
    return l

def clean_data(l,real):
    for text in l:
        if text == '':
            pass
        else:
            name = re.findall(r"\n(.+)\n", text)[0].replace(' ', '')
            # print(name)
            others = re.findall(r"\n(.+)", text)[1].split(',')
            # print(others)
            place = others[0]
            place = re.sub('\s', '', place)
            # print(place)
            age = others[1]
            age = re.sub('\s', '', age)
            # print(age)
            if len(others) >= 4:
                club = others[2:-1]
                club = ''.join(club)
                # print(club)
                club = re.sub('\s', '', club)
                point = others[-1]
                if point[0] == ' ':
                    point = point[1:]
                else:
                    point = point
            elif len(others) == 3:
                point = others[-1]
                if point[0] == ' ':
                    point = point[1:]
                else:
                    point = point
                club = ''

            total = name + ' ' + place + ' ' + age + ' ' + club + point
            print(total)
            real.append(total)


def detail_player(category,link):
    driver = selectcatogory(link,category)
    page  = driver.find_element_by_xpath('//*[@id="statistics-paging-detailed"]/div/dl[2]/dt').text
    page = page.split(' | ')[0]
    page = page.split(' ')[-1]
    page = int(page.split('/')[1])
    print(page)
    real = []
    for i in range(0, page):
        print(i+1)
        if i+1 == page:
            WebDriverWait(driver, 60, 0.5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="statistics-paging-detailed"]/div/dl[2]/dd[3]')))
            nextbutton = driver.find_element_by_xpath('//*[@id="statistics-paging-detailed"]/div/dl[2]/dd[3]')
            ActionChains(driver).move_to_element(nextbutton).click(nextbutton).perform()
            l = obtainplayer(driver)
            clean_data(l, real)
        else:
            l = obtainplayer(driver)
            # sleep(5)
            WebDriverWait(driver, 60, 0.5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="statistics-paging-detailed"]/div/dl[2]/dd[3]')))
            nextbutton = driver.find_element_by_xpath('//*[@id="statistics-paging-detailed"]/div/dl[2]/dd[3]')
            ActionChains(driver).move_to_element(nextbutton).click(nextbutton).perform()
        ###########################################
            clean_data(l, real)

                #print('Error!!!',l)
    driver.quit()
    return real
#
# link = 'https://www.whoscored.com/Regions/74/Tournaments/22/Seasons/3356/France-Ligue-1'
# category = 'tackles'
# driver = selectcatogory(link,category)
# real = detail_player(category,link)
# #print(real)



category = ['tackles','interception','fouls','cards','offsides','clearances','blocks','saves','shots','goals','dribbles','possession-loss','aerial','passes','key-passes','assists']
#
# #category = ['tackles','interception','fouls','cards','offsides','clearances','blocks','saves','shots','goals','dribbles','possession-loss','aerial','passes','key-passes','assists']
ylist = ['2012_2013']
# #ylist = ['2017_2018', '2016_2017', '2015_2016', '2014_2015', '2013_2014', '2012_2013', '2011_2012', '2010_2011']
namelist = ['France-Ligue-1']#,'Italy-Serie-A','Spain-La-Liga','Germany-Bundesliga','France-Ligue-1']
#
file = open("5.txt")

real = []
txtnamel = []



for i in namelist:
    for y in ylist:
        txtname = i+'_'+y
        txtnamel.append(txtname)

m = 0
for line in file.readlines():
    line = line.strip('\n')
    for cat in category:
        try:
            player_d = detail_player(cat,line)
            with  open(txtnamel[m]+'_'+cat+'.txt','w',encoding='utf-8') as f:
                for i in player_d:
                    f.write(i + '\n')
            print(txtnamel[m]+'_'+cat+' is finished')

        except:

            print('ERROR!!!!!' + txtnamel[m]+'_'+cat)
            traceback.print_exc()
        sleep(randint(3,7))


    m = m + 1
