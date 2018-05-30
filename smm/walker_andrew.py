# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\smm\ok')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\smm\walker')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\smm')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\\bot')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl')

from okwalker import OkWalker
from db_connect import get_db_connect_prod

from random import randint
from random import random

def main():
    db = get_db_connect_prod()
    w = OkWalker(db, '89106442900')
    w.add_friend_set_id = 2
    w.message_prob = 0.1
    w.login()
    age = randint(25, 65)
    wd = randint(1, 3)
    t = 0

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
                                                    add_to_friends=add_friend, walk_plan=plan_cnt - walked_cnt,
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