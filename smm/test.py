##from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
##from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#driver = webdriver.Chrome('D:\Distrib\python\chromedriver_win32\chromedriver.exe')
#driver.get("d:\\test\\ok.html")
#users = driver.find_elements(By.XPATH, "//div[@id = 'gs_result_list']/div")
#for x in users:
#    item = {}
#    item['id'] = x.get_attribute("data-l").split('\\,')[3]
#    node_frnd = x.find_elements(By.XPATH, './a[starts-with(@id, "hook_SwitchLayout_")]')
#r = 5

import traceback
from json import dumps

try:
    t = 6 / 0
except:
    s = traceback.format_exc()

print 123
print s
print 321

d = {'q': 1, 'w': '2', 'e': 3}

print dumps(d)

#def f(r, x):
#    r.append(x)
#    return 0

#x = []

#f(x, 1)
#print x
#f(x, 2)
#print x
