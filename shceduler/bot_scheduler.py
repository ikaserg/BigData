# -*- coding: utf-8 -*-
import datetime
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

    def add_hour(self, dt, shift):
        if dt is None:
            return None
        else:
            return dt + 1 / 24

    def trunc_hour(self, dt):
        if dt is None:
            return None
        else:
            return dt.replace(minute=0, second=0, microsecond=0)

class BotScheduler(object):
    def __init__(self, db, group):
        self.db = db
        self.group = group
        self.period = Periods()
        self.step_sql = 'select sa.start_date, sa.end_date, ' \
                        '       COALESCE(sa.shift_date, to_timestamp(\'30 Dec 1899\', \'DD Mon YYYY\')) as shift_date, ' \
                        '       COALESCE(sa.shift_time, to_timestamp(\'00:00:00\', \'HH12:MI:SS\' )::TIME) as shift_time, ' \
                        '       sa.shift, ' \
                        '       sa.bot_class_name, sa.bot_method, sa.bot_params, ap.add_period, ' \
                        '       sa.bot_method_params, ap.add_shift, ap.trunc_period, ' \
                        '       COALESCE((select ea.exe_date ' \
                        '                   from schedule.executed_bot_action ea ' \
                        '                   where ea.bot_action_id = sa.bot_action_id ' \
                        '                ), to_timestamp(\'30 Dec 1899\', \'DD Mon YYYY\')) as last_date,' \
                        '       ap.trunc_period ' \
                        '  from schedule.scheduled_bot_action sa ' \
                        ' inner join  schedule.act_periods ap on  ap.act_period_id = sa.act_period_id ' \
                        ' where now() between sa.start_date and sa.end_date ' \
                        '   and sa.group_id = %(group_id)s '\

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
                bot = globals()[act.bot_class_name](**params)
                method = getattr(bot, act.bot_method)
                if act.bot_method_params is not None:
                    params = ast.literal_eval(act.bot_method_params)
                    method(**params)
                else:
                    method()



    def loop(self):
        while True:
            self.check()

def main():
    db = get_db_connect_prod()
    sch = BotScheduler(db, 1)
    sch.check()

main()