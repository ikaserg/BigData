# -*- coding: utf-8 -*-

from okwalker import OkWalker
from db_connect import get_db_connect
import ok_api
import ok_services

class OkBot(object):
    def __init__(self, db, user_name):
        self.db = db
        self.user_name = user_name
        self.walker = OkWalker(self.db, self.user_name)
        self.social_srv =  ok_services.OkServices(ok_api.OdnoklassnikiRu(), db)
        self.social_srv.api.getDefAuth()

    def daily_bot(self):
        #проверка сообщений
        self.social_srv.appendMsgUsers()

