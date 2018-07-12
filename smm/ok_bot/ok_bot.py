# -*- coding: utf-8 -*-

from okwalker import OkWalker
from db_connect import get_db_connect
from bot import Bot
import ok_api
import ok_services

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



