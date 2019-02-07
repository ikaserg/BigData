# -*- coding: utf-8 -*-

from datetime import datetime


class SessionManager(object):
    def __init__(self, db):
        self.db = db
        self.find_sql = 'select max(s.session_id) ' \
                        '  from schedule.sessions s' \
                        ' where s.client_key = %(client_key)s '

        self.insert_sql = 'insert into schedule.sessions(session_id, dt_start, client_key) ' \
                          'values (DEFAULT, %(dt_start)s, %(client_key)s) RETURNING session_id '

        self.get_sql = 'select COALESCE(max(v.int_value), 0), max(v.varchar_value)'\
                       '  from schedule.session_variable v ' \
                       ' where v.session_id = %(session_id)s ' \
                       '   and v.variable_key = %(variable_key)s '

        self.find_var = 'select count(*)' \
                        '  from schedule.session_variable v ' \
                        ' where v.session_id = %(session_id)s ' \
                        '   and v.variable_key = %(variable_key)s '

        self.set_var_sql = 'update schedule.session_variable v ' \
                           '   set int_value = %(int_value)s, ' \
                           '       varchar_value = %(varchar_value)s ' \
                           ' where v.session_id = %(session_id)s ' \
                           '   and v.variable_key = %(variable_key)s '

        self.ins_var_sql = 'insert into schedule.session_variable(variable_key, session_id, int_value, varchar_value) ' \
                           'values (%(variable_key)s, %(session_id)s, %(int_value)s,  %(varchar_value)s )' \

        self.session_id = None

    def get_day_session(self, dt = None):
        if dt is None:
            dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        # Поиск текущей сесии
        res = self.db.do_query_one_params(self.find_sql, {'client_key': dt.strftime('%d.%m.%Y')})
        if res[0] is None:
            # Создание новой сессии
            res = self.db.do_query_one_params(self.insert_sql, {'dt_start': datetime.now(), 'client_key': dt.strftime('%d.%m.%Y')})
            self.db.commit()
        return res[0]

    def get_varchar_variable(self, key):
        return self.db.do_query_one_params(self.get_sql,
                                          {'session_id': self.session_id, 'variable_key': key})[1]

    def get_int_variable(self, key):
        return self.db.do_query_one_params(self.get_sql,
                                          {'session_id': self.session_id, 'variable_key': key})[0]

    def get_set_var_sql(self, key):
        res =  self.db.do_query_one_params(self.find_var,
                                           {'session_id': self.session_id, 'variable_key': key})
        if res[0] == 0:
            return self.ins_var_sql
        else:
            return self.set_var_sql

    def set_varchar_variable(self, key, value):
        sql = self.get_set_var_sql(key)
        self.db.exec_query_params(sql, {'session_id': self.session_id, 'variable_key': key, 'int_value': None, 'varchar_value': value})
        self.db.commit()

    def set_int_variable(self, key, value):
        sql = self.get_set_var_sql(key)
        self.db.exec_query_params(sql, {'session_id': self.session_id, 'variable_key': key, 'int_value': value, 'varchar_value': None})
        self.db.commit()


class DaySession(SessionManager):
    def __init__(self, db):
        super(DaySession, self).__init__(db)
        self.session_id = self.get_day_session()


