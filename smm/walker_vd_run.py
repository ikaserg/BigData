# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/home/etl')
sys.path.insert(0, '/home/etl/social')
sys.path.insert(0, '/home/etl/social/ok')
sys.path.insert(0, '/home/etl/social/walker')

sys.path.insert(0, '/home/common')

from okwalker import OkWalker
from db_connect import get_db_connect
from random import randint
from random import random
import db_sql

from pyvirtualdisplay import Display
from selenium import webdriver

def main():
    #display = Display(visible=0, size=(1024, 768))
    #display.start()
    import os
    os.environ['DISPLAY'] = ':77.0'

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'ru');

    browser = webdriver.Firefox(profile)

    db = get_db_connect()
    #sql = 'select * from data.social_net t where not(t.social_net_id =any(%(1)s))'
    #users = [2, 3]
    #print  db.do_query_all_params(sql, {'1': users} )
    w = OkWalker(db, '89106455257', 3, driver = browser)
    w.login()
    walked_cnt = 0
    plan_cnt = randint(30, 35)
    plan_cnt = 10
    add_prob = 1.75
    if random() < add_prob:
        add_friend = 1
    else:
        add_friend = 0
    while True:
        age = randint(25, 65)
        wd = randint(1, 3)
        if add_friend == 1:
            walk_add, add_friend = w.find_user_list(from_age = str(age), till_age = str(age+wd), location='Рязань',
                                                    add_to_friends = add_friend, gender = 'f', walk_plan = plan_cnt - walked_cnt,
                                                    limit_stop = True, )
            if add_friend == 0:
                break
        else:
            walk_add, add_friend = w.find_user_list(from_age=str(age), till_age=str(age + wd), location='Рязань',
                                           walk_plan = plan_cnt - walked_cnt)
        walked_cnt += walk_add
        if walked_cnt >= plan_cnt:
            break

    browser.quit()
    #display.stop()

main()