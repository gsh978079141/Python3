'''
Created on 2018年4月11日

@author: gdd
'''
# coding = utf-8
from selenium import webdriver
import time

dr = webdriver.Chrome(executable_path="D:\Python\chromedriver.exe")
try:
    dr.get("http://www.panda.tv")
    dr.implicitly_wait(15)
    print(dr.title)
    dr.find_element_by_link_text("登录").click()
    time.sleep(3)
    ele = dr.find_element_by_xpath("//*[@id='ruc_dialog_container']/div[2]/div/div[1]/div/input").send_keys("username")
    ele = dr.find_element_by_xpath("//*[@id='ruc-input-password-field']").send_keys("password")
    time.sleep(3)
    dr.find_element_by_xpath("//*[@id='ruc_dialog_container']/div[2]/div/div[6]").click()
    time.sleep(3)
    print("登录成功")
    dr.get("http://www.panda.tv/101010")
    dr.implicitly_wait(15)
    print(dr.title)
    while(i1):
        dr.find_element_by_xpath("//*[@id='main-container']/div[2]/div[4]/div[2]/div[1]/textarea").send_keys("你想说的话")
        time.sleep(5)
        dr.find_element_by_xpath("//*[@id='main-container']/div[2]/div[4]/div[2]/div[2]").click()
    dr.quit()
except Exception as e:
    print(e)