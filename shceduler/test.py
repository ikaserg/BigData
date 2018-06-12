# -*- coding: utf-8 -*-
import datetime
import ok_bot
from db_sql import filed_by_names
from db_connect import get_db_connect
from db_connect import get_db_connect_prod

class Periods(object):
    def __init__(self):
        None

    def add_month(self, dt, shift):
        return dt + 30

    def add_week(self, dt, shift):
        return dt + 7

    def add_day(self, dt, shift):
        return dt + 1

    def add_hour(self, dt, shift):
        return dt + 1 / 24

    def trunc_hour(self, dt):
        return dt.replace(minute=0, second=0, microsecond=0)

class A(object):
    def __init__(self):
        self.msg = 'Hellow World!'
        self.p = Periods()

    def method(self):
        print(self.msg)
        mp = getattr(self.p, 'trunc_hour')
        print(mp(datetime.datetime.now()))

a = A()
m = getattr(a, u'method')
m()

sql = 'select t.* from schedule.scheduled_bot_action t'
db = get_db_connect_prod()
acts = db.do_query_all_fbn(sql)
for act in acts:
    print(act.shift)