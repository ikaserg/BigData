# -*- coding: utf-8 -*-

from okwalker import OkWalker
from okwalker import OkUserFilter
from okwalker import OK_FRIENDS_FILTER_URL
from db_connect import get_db_connect
from bot import Bot
import ok_api
import ok_services
import datetime

from random import randint
from random import random

class OkBot(Bot):
    def __init__(self, db, session, user_name):
        self.db = db
        self.session = session
        self.user_name = user_name
        self.bot_id = 1
        self.walker = OkWalker(self.db, self.user_name)
        self.social_srv =  ok_services.OkServices(ok_api.OdnoklassnikiRu(), db)
        self.social_srv.api.getDefAuth()
        self.is_logged = False
        self.stop_limit = 2

    def login(self):
        if not self.is_logged:
            self.walker.login()
            self.is_logged = True

    def find_random_user(self):
        if not self.is_logged:
            self.login()
        time_start = datetime.datetime.now().time()
        walked_cnt = 0
        plan_cnt = 5
        zero_max = 15

        add_prob = 1.75
        if random() < add_prob:
            add_friend = 1
        else:
            add_friend = 0

        age = randint(25, 65)
        wd = randint(1, 3)
        filter = OkUserFilter(walker = self.walker, gender='f', from_age=str(age), till_age=str(age + wd),\
                              location='г. Рязань (Рязанская область)', online = True)
        friend_cnt = 0
        stop_count = self.session.get_int_variable('daily_stop_count')
        run = (stop_count < self.stop_limit)
        while run:
            age = randint(25, 65)
            wd = randint(1, 3)
            filter.apply_filter(gender='f', from_age=str(age), till_age=str(age + wd), location='г. Рязань (Рязанская область)', online = True)
            cnt, add_cnt, stop = self.walker.apply_user_list(filter, self.walker.add_friend_handler, plan_cnt - friend_cnt, OK_FRIENDS_FILTER_URL)
            friend_cnt = friend_cnt + add_cnt
            if stop :
                self.session.set_int_variable('daily_stop_count', stop_count + 1)
            run = not stop and (friend_cnt < plan_cnt)

    def load_all_message(self):
        if not self.is_logged:
            self.login()
        self.walker.load_all_message(5, self.walker.was_read)
        #загрузка пользователнй сообщений
        self.social_srv.appendMsgUsers()

    def daily_bot(self):
        #проверка сообщений
        self.walker.login()
        self.walker.load_all_message(20, self.walker.was_read)
        #загрузка пользователнй сообщений
        self.social_srv.appendMsgUsers()
