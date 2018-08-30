# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
from bot_logger import BotLogger
import datetime
import sys

from selenium.webdriver.common.by import By

from time import sleep

WALKER_FIENDS = 1001
WALKER_START_FIENDS = 1002
WALKER_STOP_FIENDS = 1003

REL_COMMON = 0
REL_FRIEND = 1
REL_VISIT = 2
REL_PLAN_INVITE = 3
REL_INVITE = 4
REL_FRIEND_OUT = 6

ACT_SKIP = 0
ACT_DONE = 1
ACT_STOP = -1

INV_ERROR = -1
INV_OK = 0
INV_ALREADY = 2
INV_TEMPORARY_CANNONT = 3


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

        self.invite_try_cnt = 3

    def get_last_user_status(self, user_id):
        sql = 'select max(t.relation_type_id)' \
              '  from social.user_relations t ' \
              ' where t.social_net_id = %(social)s' \
              '   and t.user_id = %(user_id)s' \
              '   and t.rel_user_id = %(rel_user_id)s'\
              '   and t.relation_date = (select max(t_i.relation_date) ' \
              '                            from social.user_relations t_i ' \
              '                           where t_i.social_net_id = t.social_net_id ' \
              '                             and t_i.user_id = t.user_id ' \
              '                             and t_i.rel_user_id = t.rel_user_id)'
        return self.db.do_query_all_params(sql, {'user_id': self.user_id, 'social': self.social_id,
                                                               'rel_user_id': user_id})[0][0]
    def log_friend_list_start(self):
        self.logger.write_log(WALKER_START_FIENDS,
                              0,
                              'Start',
                              '')
        self.logger.stop_event()

    def log_friend_list_stop(self, handle_cnt, do_cnt, limit_stop):
        self.logger.write_log(WALKER_STOP_FIENDS,
                              0,
                              'Stop, ' + self.logger.dumps({'handled': handle_cnt, 'do action': do_cnt, 'limit stop': limit_stop}),
                              '')
        self.logger.stop_event()

    def add_friend_handler(self, user, html_user, last_rel):
        if (user['rel'] == REL_COMMON) and \
                (last_rel is None or last_rel not in [REL_FRIEND, REL_INVITE, REL_FRIEND_OUT]):
            # Отправка приглащения в друзья
            add_res = self.add_to_friend(user, html_user, self.driver.current_window_handle, self.invite_try_cnt)
            if add_res == INV_OK:
                user['rel'] = REL_INVITE
                return ACT_DONE
            elif add_res == INV_TEMPORARY_CANNONT:
                return ACT_STOP
        else:
            return ACT_SKIP

    # Формирует список пользователей и вызывает для них  функцию
    def apply_user_list(self, filter, handler, walk_plan = 30, url = None):
        self.logger.start_event()
        self.log_friend_list_start()
        self.walk_plan = walk_plan
        last_user = 0
        do_cnt = 0
        self.driver.get(url)
        filter.fill_filter()
        sleep(2)
        r = None
        try:
            run = True
            while run:
                users = self.driver.find_elements(By.XPATH, self.xpath_user_list)
                for x in users[last_user:]:
                    last_user = last_user + 1
                    # скролл, что бы пользователь был в видимой части окна
                    self.center_scroll(x)
                    item = self.parse_user_params(x)
                    # Получаем текущий статус пользователя в БД
                    last_rel = self.get_last_user_status(item['id'])
                    # Вызов функции обработки
                    r = handler(item, x, last_rel)
                    run = r <> ACT_STOP
                    if r == ACT_DONE:
                        do_cnt = do_cnt + 1
                        run = run and do_cnt < walk_plan
                    if (last_rel is None or (last_rel <> item['rel'])) and (item['rel'] <> REL_COMMON):
                        # Зпись нового статуса
                        self.add_users_rel([item], datetime.datetime.now())
                    if not run:
                        break
                self.scroll_user_list()
            self.log_friend_list_stop(last_user, do_cnt, r == ACT_STOP)
        except Exception as err:
            self.logger.write_execption
            print sys.exc_info()

        return last_user, do_cnt, r == ACT_STOP


class WalkerUserFilter(object):
    def __init__(self, walker, gender, from_age, till_age, location, online):
        self.walker = walker
        self.gender = gender
        self.from_age = from_age
        self.till_age = till_age
        self.location = location
        self.online = online

    def pause(self):
        sleep(1)

    def fill_filter(self, cont):
        self.fill_gender(cont)
        self.fill_from_age(cont)
        self.fill_till_age(cont)
        self.fill_location(cont)
        self.fill_online(cont)


    def apply_filter(self, gender, from_age, till_age, location, online, url = None):
        self.gender = gender
        self.from_age = from_age
        self.till_age = till_age
        self.location = location
        self.online = online



