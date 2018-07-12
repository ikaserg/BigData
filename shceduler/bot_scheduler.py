# -*- coding: utf-8 -*-
import sys
import math
import datetime
from time import sleep
from ok_bot import OkBot
from db_sql import filed_by_names
from db_connect import get_db_connect
from db_connect import get_db_connect_prod
import ast

class Periods(object):
    def __init__(self):
        None

    def add_month(self, dt, shift):
        if dt is None:
            return None
        else:
            return dt + 30

    def add_week(self, dt, shift):
        if dt is None:
            return None
        else:
            return dt + 7

    def add_day(self, dt, shift):
        if dt is None:
            return None
        else:
            return dt + datetime.timedelta(days = shift)

    def add_10_minutes(self, dt, shift):
        if dt is None:
            return None
        else:
            return dt + datetime.timedelta(minutes = shift * 10)

    def add_hour(self, dt, shift):
        if dt is None:
            return None
        else:
            return dt + datetime.timedelta(hours = shift)

    def trunc_hour(self, dt):
        if dt is None:
            return None
        else:
            return dt.replace(minute=0, second=0, microsecond=0)

    def trunc_10_minute(self, dt):
        if dt is None:
            return None
        else:
            return dt.replace(minute=math.trunc(dt.minute * 10) / 10, second=0, microsecond=0)

    def current_day(self, dt):
        return datetime.datetime.now().replace(hour = 0, minute=0, second=0, microsecond=0)

    def do_nothing(self, dt, shift):
        return dt



class BotScheduler(object):
    def __init__(self, db, group):
        self.db = db
        self.group = group
        self.period = Periods()
        self.class_list = {}
        self.step_sql = 'select sa.start_date, sa.end_date, ' \
                        '       sa.bot_action_id, ' \
                        '       COALESCE(sa.shift_date, to_timestamp(\'30 Dec 1899\', \'DD Mon YYYY\')) as shift_date, ' \
                        '       COALESCE(sa.shift_time, to_timestamp(\'00:00:00\', \'HH12:MI:SS\' )::TIME) as shift_time, ' \
                        '       sa.shift, ' \
                        '       sa.bot_class_name, sa.bot_method, sa.bot_params, ap.add_period, ' \
                        '       sa.bot_method_params, ap.add_shift, ap.trunc_period, ' \
                        '       COALESCE((select max(ea.exe_date) ' \
                        '                   from schedule.executed_bot_action ea ' \
                        '                   where ea.bot_action_id = sa.bot_action_id ' \
                        '                ), to_timestamp(\'30 Dec 1899\', \'DD Mon YYYY\')) as last_date,' \
                        '       ap.trunc_period ' \
                        '  from schedule.scheduled_bot_action sa ' \
                        ' inner join  schedule.act_periods ap on  ap.act_period_id = sa.act_period_id ' \
                        ' where now() between sa.start_date and sa.end_date ' \
                        '   and sa.group_id = %(group_id)s ' \
                        ' order by sa.act_order '\

        self.exe_sql = 'insert into schedule.executed_bot_action(bot_action_id, bot_id, exe_date, result_id, result_message) ' \
                       ' values( %(bot_action_id)s , %(bot_id)s, %(exe_date)s , %(result_id)s , %(result_message)s  )'

    def write_executed(self, dt, bot_id, bot_action_id, result, message):
        self.db.exec_query_params(self.exe_sql, {'bot_action_id': bot_action_id,
                                                 'bot_id': bot_id,
                                                 'exe_date': dt,
                                                 'result_id': result,
                                                 'result_message': message
                                                 })
        self.db.exec_query('commit')

    def check(self):
        acts = self.db.do_query_all_fbn_params(self.step_sql, {'group_id': self.group})
        for act in acts:
            self.period.trunc_hour(datetime.datetime.now())
            trunc_period = getattr(self.period, act.trunc_period)
            add_period = getattr(self.period, act.add_period)
            if add_period(trunc_period(act.last_date), 1).replace(tzinfo = None) + act.shift <= datetime.datetime.now():
                params ={'db': self.db}
                bot_prs = ast.literal_eval(act.bot_params)
                for key in bot_prs:
                    params[key] = bot_prs[key]
                # Был ли уже сссоздан такой объект
                if act.bot_class_name+'(' + act.bot_params + ')' in self.class_list:
                    bot = self.class_list[act.bot_class_name+'(' + act.bot_params + ')']
                else:
                    bot = globals()[act.bot_class_name](**params)
                    self.class_list[act.bot_class_name+'(' + act.bot_params + ')'] = bot
                method = getattr(bot, act.bot_method)
                start_date = datetime.datetime.now()
                #try:
                self.write_executed(start_date, bot.bot_id, act.bot_action_id, 0, '')
                if act.bot_method_params is not None:
                    params = ast.literal_eval(act.bot_method_params)
                    method(**params)
                else:
                    method()
                #self.write_executed(start_date, bot.bot_id, act.bot_action_id, 0, '')
                #except Exception as ex:
                #    self.write_executed(start_date, bot.bot_id, act.bot_action_id, -1, sys.exc_info()[0])



    def loop(self):
        while True:
            self.check()

def main():
    db = get_db_connect_prod()
    sch = BotScheduler(db, 1)
    while True:
        sch.check()
        sleep(60)

main()