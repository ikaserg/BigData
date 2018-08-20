# -*- coding: utf-8 -*-

from okwalker import OkWalker
from db_connect import get_db_connect
from bot import Bot
import ok_api
import ok_services
import datetime

from random import randint
from random import random

class OkBot(Bot):
    def __init__(self, db, user_name):
        self.db = db
        self.user_name = user_name
        self.bot_id = 1
        self.walker = OkWalker(self.db, self.user_name)
        self.social_srv =  ok_services.OkServices(ok_api.OdnoklassnikiRu(), db)
        self.social_srv.api.getDefAuth()
        self.is_logged = False

    def login(self):
        if not self.is_logged:
            self.walker.login()
            self.is_logged = True

    def find_random_user(self):
        if not self.is_logged:
            self.login()
        time_start = datetime.datetime.now().time()
        walked_cnt = 0
        plan_cnt = 3
        zero_max = 15

        add_prob = 1.75
        if random() < add_prob:
            add_friend = 1
        else:
            add_friend = 0
        zero_cnt = 0

        limit_stop = False
        while not limit_stop:
            age = randint(25, 65)
            wd = randint(1, 3)
            if add_friend == 1:
                walk_add, add_friend, limit_stop = self.walker.find_user_list(from_age=str(age), till_age=str(age + wd), location='г. Рязань (Рязанская область)',
                                                                  add_to_friends=add_friend, gender='f', walk_plan=plan_cnt - walked_cnt )
                if add_friend == 0:
                    break
            else:
                walk_add, add_friend, limit_stop = self.walker.find_user_list(from_age=str(age), till_age=str(age + wd), location='г. Рязань (Рязанская область)',
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

    def load_all_message(self):
        if not self.is_logged:
            self.login()
        self.walker.load_all_message(20, self.walker.was_read)
        #загрузка пользователнй сообщений
        self.social_srv.appendMsgUsers()


    def daily_bot(self):
        #проверка сообщений
        self.walker.login()
        self.walker.load_all_message(20, self.walker.was_read)
        #загрузка пользователнй сообщений
        self.social_srv.appendMsgUsers()



