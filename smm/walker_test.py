# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\smm\ok')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\smm\walker')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\smm')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\\bot')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl')

from okwalker import OkWalker
from db_connect import get_db_connect
from db_connect import get_db_connect_prod
from random import randint
import db_sql

from random import randint
from random import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def main():
    db = get_db_connect_prod()
    #sql = 'select * from data.social_net t where not(t.social_net_id =any(%(1)s))'
    #users = [2, 3]
    #print  db.do_query_all_params(sql, {'1': users} )
    w = OkWalker(db, '89106455257')
    #r = w.handled_users([1, 2, 3])
    w.login()
    #w.driver.execute_script("window.open('', 'new_window')")
    #actions = ActionChains(w.driver)
    #w.driver.find_element_by_tag_name('body').click()
    #actions.key_down(Keys.CONTROL).key_down('t').key_up('t').key_up(Keys.CONTROL).perform()
    #ActionChains(w.driver).send_keys(Keys.CONTROL, 't')
    #w.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, 't')
    #w.driver.close()

    #w.find_user_list(gender = 'f')
    age = randint(25, 65)
    wd = randint(1, 3)
    #w.find_user_list(from_age = str(age), till_age = str(age+wd), location='Рязань', add_to_friends = 1, walk_plan = 5)
    #w.find_user_list(from_age = '38', till_age = '39', location='Рязань', add_to_friends = 1)
    #url_test = 'd:/test/friend_added.html'
    ##url_test = 'D:/test/ok_user.html'
    ##w.driver.get(url_test)
    ##r = w.send_invite()
    t = 0
    #w.find_user_list(from_age = '43', till_age = '47', location='Рязань')
    #w.assertIn("Гринина", w.driver.page_source)

    walked_cnt = 0
    plan_cnt = 1
    zero_max = 5

    add_prob = 1.75
    if random() < add_prob:
        add_friend = 1
    else:
        add_friend = 0

    zero_cnt = 0

    while True:
        age = randint(25, 65)
        wd = randint(1, 3)
        if add_friend == 1:
            walk_add, add_friend = w.find_user_list(from_age=str(age), till_age=str(age + wd), location='Рязань',
                                                    add_to_friends=add_friend, gender='f', walk_plan=plan_cnt - walked_cnt,
                                                    limit_stop=True )
            if add_friend == 0:
                break
        else:
            walk_add, add_friend = w.find_user_list(from_age=str(age), till_age=str(age + wd), location='Рязань',
                                                    walk_plan=plan_cnt - walked_cnt)
        walked_cnt += walk_add

        if walk_add == 0:
            zero_cnt += 1
        else:
            zero_cnt = 0

        if zero_cnt >= zero_max:
            break

        if walked_cnt >= plan_cnt:
            break

main()