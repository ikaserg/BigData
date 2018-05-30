# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
from bot_logger import BotLogger

WALKER_FIENDS = 1001
WALKER_START_FIENDS = 1002
WALKER_STOP_FIENDS = 1003

class Walker(object):
    def __init__(self, db, user_name, social_id, driver = None):
        #display = Display(visible=0, size=(1024, 768))
        #display.start()

        #self.driver = webdriver.Firefox()
        if driver is None:
            #self.driver = webdriver.Chrome('D:\Distrib\python\chromedriver_win32\chromedriver.exe')
            self.driver = webdriver.Chrome('C:\Distrib\python\chromedriver.exe')
        else:
            self.driver = driver

        self.db = db
        self.user_name = user_name
        self.social_id = social_id
        # select password
        sql = "select ua.user_password, ua.user_id" \
              "  from social.users_auth ua" \
              " where ua.social_net_id = %(social)s" \
              "   and ua.user_login = %(uname)s";
        res = db.do_query_one_params(sql, {'uname': self.user_name, 'social': self.social_id})
        self.user_password = res[0]
        self.user_id = res[1]

        self.logger = BotLogger(self.db, self.bot_id)

