# -*- coding: utf-8 -*-

LIMIT_STOP = 1

import sys
#import win32com.client as comclt
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui
from time import sleep

import win32com.client as comctl

from random import random

from copy import copy

from walker import WALKER_FIENDS
from walker import WALKER_START_FIENDS
from walker import WALKER_STOP_FIENDS

from walker import REL_COMMON
from walker import REL_FRIEND
from walker import REL_VISIT
from walker import REL_PLAN_INVITE
from walker import REL_INVITE
from walker import REL_FRIEND_OUT

from walker import ACT_SKIP
from walker import ACT_DONE
from walker import ACT_STOP

from walker import INV_ERROR
from walker import INV_OK
from walker import INV_ALREADY
from walker import INV_TEMPORARY_CANNONT

from walker import Walker
from walker import WalkerUserFilter
import datetime
from lxml import etree
from io import StringIO, BytesIO

import ok_api

import pickle

OK_FRIENDS_FILTER_URL = 'https://ok.ru/search?st.mode=Users&st.vpl.mini=false&st.onSite=on&st.grmode=Groups&st.posted=set'
OK_MESSAGES_URL = 'https://ok.ru/messages'
OK_MESSAGES_URL = 'https://ok.ru/messages'

class OkUserFilter(WalkerUserFilter):
    def __init__(self, walker, gender, from_age, till_age, location, online):
        self.walker = walker
        self.gender = gender
        self.from_age = from_age
        self.till_age = till_age
        self.location = location
        self.online = online
        self.sex_tag = 'div'

    def fill_filter(self):
        # переход в начало страницы
        self.walker.driver.execute_script("window.scrollTo(0, 20);")
        sleep(3)
        flts = self.walker.driver.find_elements_by_class_name("gs_filter_list")
        super(OkUserFilter, self).fill_filter(flts)
        sleep(5)
        self.walker.logger.write_log(WALKER_FIENDS,
                                     0,
                                     self.walker.logger.dumps(
                                                        {'gender': self.gender,
                                                         'from_age': self.from_age,
                                                         'till_age': self.till_age,
                                                         'location': self.location,
                                                         'on_site': self.online,
                                                         'walk_plan': self.walker.walk_plan}),
                                     '')

    def fill_gender(self, cont):
        self.pause()
        if self.gender is not None:
            lst = cont[0].find_elements_by_tag_name('li')
            if self.gender == 'm':
                lst[1].find_element_by_tag_name(self.sex_tag).click()
            if self.gender == 'f':
                lst[2].find_element_by_tag_name(self.sex_tag).click()

    def fill_from_age(self, cont):
        if self.from_age is not None:
            elem = Select(cont[1].find_elements_by_tag_name('select')[0])
            elem.select_by_value(self.from_age)

    def fill_till_age(self, cont):
        if self.till_age is not None:
            elem = Select(cont[1].find_elements_by_tag_name('select')[1])
            elem.select_by_value(self.till_age)

    def fill_location(self, cont):
        if self.location is not None:
            i = 0
            while i < 3:
                try:
                    # до 15.12.2016 был тэг спан
                    elem = cont[2].find_element_by_xpath("li/div[@data-field_location='" + self.location +
                                                         "' and @data-field_country='10414533690']")
                    self.walker.center_click(elem)
                    break
                except:
                    self.walker.driver.execute_script("window.scrollTo(0, 20);")
                    i += 1
            if i >= 3:
                # до 15.12.2016 был тэг спан
                elem = cont[2].find_element_by_xpath("li/div[@data-field_location='" + self.location +
                                                     "' and @data-field_country='10414533690']")
                elem.click()

    def fill_online(self, cont):
        if self.online is not None:
            wait = WebDriverWait(self.walker.driver, 50)
            # elem = wait.until(EC.element_to_be_clickable((By.ID, 'field_onSite')))
            elem = cont[9].find_element_by_id('field_onSite')
            elem_m = cont[9].find_element_by_id('field_refs')
            elem = wait.until(EC.visibility_of_element_located((By.ID, 'field_onSite')))
            if self.online != elem.is_selected():
                elem.click()


class Object(object):
    pass

class OkWalker(Walker):
    def __init__(self, db, user_name, social_id = 3, driver = None):
        self.bot_id = 1
        super(OkWalker, self).__init__(db, user_name, social_id, driver)

        self.api = ok_api.OdnoklassnikiRu()
        self.api.getDefAuth()
        self.fields = 'first_name,last_name,gender,birthday,location,current_status,' \
                      'current_status_id,current_status_date,url_profile,allows_anonym_access,' \
                      'registered_date,premium'

        self.class_prob = 0.75
        self.vote_prob = 0.75
        self.message_prob = 0
        self.add_friend_set_id = 1

        self.xpath_user_list = "//div[@id = 'gs_result_list']//div[contains(@class, 'gs_result_i_w')]"
        self.xpath_show_more = "//div[@id = 'hook_Block_ConversationsList']//a[@data-show-more='link-show-more']"
        self.xpath_user_link = ".//div[contains(@class, 'gs_result_i_t')]//a[starts-with(@hrefattrs, 'st.cmd=friendMain')]"


    def login(self):
        self.driver.get("https://ok.ru/")
        #set user name
        elem = self.driver.find_element_by_name("st.email")
        elem.send_keys(self.user_name)

        # set password
        elem = self.driver.find_element_by_name("st.password")
        elem.send_keys(self.user_password)
        elem.send_keys(Keys.RETURN)

    def get_user_page(self, user_id):
        return "https://ok.ru/profile/{0}/".format(user_id)

    def open_user_page(self, user_id):
        self.driver.get("https://ok.ru/profile/{0}/".format(user_id))
        return 0

    def getIntWordByInd(self, text, ind = 0, sep = ' '):
        if len(text) > 0:
            lst = text[0].split(sep)
            ind_t = ind
            if ind_t < 0:
                ind_t = ind_t + 1
            if len(lst) > abs(ind_t):
                return int(lst[ind].replace(u'\xa0', u''))
            else:
                return 0
        else:
            return 0

    def commit(self):
        return self.db.exec_query('commit;')

    def add_message(self, mess):
        sql_sel = 'select count(*) '\
                  '  from social.messages '\
                  ' where from_user_id = %(from_user_id)s '\
                  '   and to_user_id = %(to_user_id)s '\
                  '   and message_date_int = %(message_date_int)s '

        d = self.db.do_query_all_params(sql_sel, {'from_user_id': mess.from_user_id,
                                                  'to_user_id': mess.to_user_id,
                                                  'message_date_int': mess.message_date_int})

        if d[0][0] == 0:
            sql = 'insert into social.messages(thread_id, social_net_id, from_user_id, to_user_id, ' \
                  '                            message_date, message, message_uuid, message_date_int) ' \
                  'values(%(thread_id)s, %(social_net_id)s, %(from_user_id)s, %(to_user_id)s, %(message_date)s,' \
                  '       %(message)s, %(message_uuid)s, %(message_date_int)s) '

            self.db.exec_query_params(sql, {'thread_id': mess.thread_id,
                                            'social_net_id': self.social_id,
                                            'from_user_id': mess.from_user_id,
                                            'to_user_id': mess.to_user_id,
                                            'message_date': mess.message_date,
                                            'message': mess.message,
                                            'message_uuid': mess.message_uuid,
                                            'message_date_int': mess.message_date_int})

    def was_read(self, node):
        xpath_not = ".//div[contains(@class,  'notification')]/div[@class = 'counterText']"
        return len(node.find_elements(By.XPATH, xpath_not)) == 0

    def scroll_user(self):
        None

    def load_all_message(self, max_loaded = 0, filter = None):
        # open messages page
        self.driver.get(OK_MESSAGES_URL)
        last_user = 0

        sql_last_updade_sel = 'select max(message_date_int) ' \
                              '  from social.messages ' \
                              ' where from_user_id = %(user_id)s ' \
                              '    or to_user_id = %(user_id)s '
        loaded_cnt = 0
        while True:
            if (loaded_cnt >= max_loaded) and (max_loaded > 0):
                break
            # Получаем список пользователей
            wrap_xpath = "//div[@id = 'hook_Block_ConversationContent']"
            users_wrap_xpath = "//div[@id = 'hook_Block_ConversationsList']"
            xpath = "//div[@id = 'hook_Block_ConversationsList']//div[@tsid = 'conversation_item']"
            #xpath = "//div[@id = 'hook_Block_ConversationsList']//div[starts-with(@id, 'hook_Block_PRIVATE_')]"
            msg_xpath = "//div[@id = 'hook_Block_ConversationContent']//div[starts-with(@id, 'PRIVATE_')]"
            txt_xpath = ".//span[starts-with(@id, 'hook_ActivateLinks_')]"
            show_more_xpath = "//div[@id = 'hook_Block_ConversationsList']//a[@data-show-more='link-show-more']"
            users = self.driver.find_elements(By.XPATH, xpath)
            users_wrap =  self.driver.find_element(By.XPATH, users_wrap_xpath)

            show_more = self.driver.find_element(By.XPATH, show_more_xpath)
            sleep(4)
            self.driver.execute_script("return arguments[0].scrollIntoView(true);", show_more)

            for user in users[last_user:]:
                if (loaded_cnt >= max_loaded) and (max_loaded > 0):
                    break
                last_user += 1
                if (filter is None) or (filter(user)):
                    user_id = user.get_attribute('data-id').split('_')[1]
                    user.click()
                    sleep(3)
                    # Поиск последнего загруженного собщения
                    last_msg_date = self.db.do_query_all_params(sql_last_updade_sel, {'user_id': user_id})[0][0]
                    if (last_msg_date is None) or  (int(last_msg_date) <  int(user.get_attribute('data-updated'))):
                        wrap = self.driver.find_element(By.XPATH, wrap_xpath)
                        msg_cnt = 0
                        while True:
                            # Получение списка сообщений
                            msgs = self.driver.find_elements(By.XPATH, msg_xpath)
                            if len(msgs) < 4:
                                break
                            if len(msgs) == msg_cnt:
                                break
                            else:
                                msg_cnt = len(msgs)
                                self.driver.execute_script('arguments[0].scrollTop = 0', wrap)
                                self.driver.execute_script('arguments[0].scrollTop = 0', wrap)
                                sleep(3)
                                #.location_once_scrolled_into_view
                                #wrap.send_keys(Keys.PAGE_UP)
                        for msg in msgs:
                            msg_info = Object()
                            #if '__me' in msg.get_attribute('class').split(' '):
                            msg_info.message_uuid =  msg.get_attribute('data-uuid')

                            if msg.get_attribute('data-mine') == "true":
                                msg_info.to_user_id = user_id
                                msg_info.from_user_id = self.user_id
                            else:
                                msg_info.to_user_id = self.user_id
                                msg_info.from_user_id = user_id
                            msg_info.message_date = datetime.datetime.fromtimestamp(long(msg.get_attribute('data-created')) / 1000.0)
                            msg_info.message_date_int = long(msg.get_attribute('data-created'))
                            try:
                                msg_info.message = msg.find_element(By.XPATH, txt_xpath).text
                            except:
                                msg_info.message = ''
                            msg_info.thread_id = None
                            print msg_info
                            self.add_message(msg_info)
                        self.commit()
                    else:
                        loaded_cnt = loaded_cnt + 1
                else:
                    self.scroll_user()
            # поиск кнопки "Показать еще"
            #self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', users_wrap)
            #show_more = self.driver.find_element(By.XPATH, show_more_xpath)
            #sleep(4)
            #show_more.click()

    def not_handled_users(self, user_list, rel):
        t = 6
        sql = 'select t.rel_user_id' \
              '  from social.user_relations t ' \
              ' where t.social_net_id = %(social)s' \
              '   and t.user_id = %(user_id)s' \
              '   and t.relation_type_id =any (%(rel)s)' \
              '   and  (t.rel_user_id =any(%(user_list)s))'

        res = [x[0] for x in self.db.do_query_all_params(sql, {'user_id': self.user_id, 'social': self.social_id,
                                                               'rel': rel, 'user_list': user_list})]
        return [x for x in user_list if x not in res]

    def add_users_rel(self, user_list, rel_date):
        t = 6
        sql = 'insert into social.user_relations(social_net_id, user_id, rel_user_id, ' \
              '  relation_date, relation_type_id, int_param1, int_param2, int_param3, int_param4, int_param5 ) ' \
              'values (%(social_net_id)s, %(user_id)s, %(rel_user_id)s, %(relation_date)s, ' \
              '  %(relation_type)s, %(p1)s, %(p2)s, %(p3)s, %(p4)s, %(p5)s)'
        for user in user_list:
            self.db.exec_query_params(sql,
                                      {'social_net_id': self.social_id, 'user_id':self.user_id, 'rel_user_id': user['id'],
                                       'relation_date': rel_date, 'relation_type': user['rel'], 'p1': user['p1'], 'p2': user['p2'],
                                       'p3': user['p3'], 'p4': user['p4'], 'p5': user['p5']})
        return self.db.exec_query('commit;')

    def open_new_tab_user_link(self, user, html_user, main_window):
        #self.driver.execute_script("window.open('"+self.get_user_page(user['id'])+"', 'new_window')")
        #self.driver.find_element_by_id('gs_result_list').click()
        user_link = html_user.find_elements(By.XPATH, self.xpath_user_link)
        if len(user_link) > 0:
            actions = ActionChains(self.driver)
            actions.move_to_element(user_link[0]).context_click().perform()
            wsh = comctl.Dispatch("WScript.Shell")
            wsh.SendKeys("{DOWN}")
            wsh.SendKeys("{DOWN}")
            wsh.SendKeys("{ENTER}")
            handle = self.driver.window_handles[-1]
            self.driver.switch_to_window(handle)
            return handle
        else:
            return None

    def close_tab(self, tab_handle, main_window):
        self.driver.switch_to_window(tab_handle)
        self.driver.close()
        self.driver.switch_to_window(main_window)
        return 0

    def close_current_tab(self, main_window):
        self.driver.close()
        self.driver.switch_to_window(main_window)
        return 0

    def avatar_class(self):
        # поиск элемента аватарки
        ava = self.driver.find_element(By.XPATH, "//div[contains(@class, 'lcTc_avatar')]")
        # проверка можно ли ставить классы
        class_hook = ava.find_elements(By.XPATH, ".//div[starts-with(@id, 'hook_Block_')]")
        if len(class_hook) > 0:
            # проверка нет ли уже класса
            elem = class_hook[0].find_elements(By.XPATH, ".//span[contains(@class, 'tico')]")[0]
            if elem.text == u'Вы':
                # alredy has class
                return 2
            else:
                if elem.text == u'Класс!':
                    #send class
                    elem.click()
                    return 0
                else:
                    # unknow situation
                    return 3
        else:
            # Class is locked
            return 1
        return 0

    def avatar_vote(self):
        # open avatar photo
        # поиск элемента аватарки
        ava = self.driver.find_element(By.XPATH, "//div[contains(@class, 'lcTc_avatar')]")
        # проверка есть ли сылка на изображение
        img = ava.find_elements(By.XPATH, ".//a[@class='card_wrp']")
        if len(img) > 0:
            # переход на страницу с аватаркой
            img[0].click()
            sleep(3)
            vote_5 = self.driver.find_elements(By.XPATH, "//div[@id='hook_Block_PopLayerViewFriendPhotoRating']/a[text()='5']")
            if len(vote_5) > 0:
                vote_5[0].click()
                res = 0
            else:
                # Alredy voted
                res = 2
            # close vote window
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'photo-layer_close')]").click()
            sleep(3)
            return res
        else:
            # Vote is locked
            return 1

    def select_message(self, mes_set_id):
        # Получение случайного сообщения
        sql = 'select it.message_prob, m.message, m.bot_message_id ' \
              ' from social.bot_message_set_items it ' \
              'inner join social.bot_messages m on m.bot_message_id = it.bot_message_id ' \
              'where it.bot_message_set_id = %(message_set)s '

        p = random()
        ms = self.db.do_query_all_params(sql, {'message_set': mes_set_id})
        i = 0
        tp = 0
        while (tp < p) and (i < len(ms)):
            tp = ms[i][0]
            i += 1
        self.send_message(ms[i - 1][1])
        return ms[i - 1][2]

    # Вовращает значение
    # -1 - ошибка при добавлении
    # 0 - успешно добавлено
    # 3 - временно нельзя добавить
    def send_invite(self):
        # Find add user button
        btn = self.driver.find_elements(By.XPATH,
                                        u'//div[contains(@data-l, "tc_friend")]/ul/li/a[contains(@href, "dk?cmd=MiddleColumnTopCardFriend")]')
        if len(btn) == 0:
            btn = self.driver.find_elements(By.XPATH, u"//div[contains(@class, 'u-menu_li__pro')]/a/span[text()='Добавить в друзья']")
            if len(btn) == 0:
                btn = self.driver.find_elements(By.XPATH, u"//div[contains(@class, 'u-menu_li__pro')]/a[text()='Добавить в друзья']")
        if len(btn) > 0:
            btn[0].click()
            sleep(2)
            err = self.driver.find_elements(By.XPATH, "//div[@id='notifyPanel_msgContainer']")
            if len(err) > 0:
                #Can not add
                return INV_TEMPORARY_CANNONT
            else:
                # find add confirmation
                res = self.driver.find_elements(By.XPATH,
                                                u'//div[contains(@data-l, "tc_friend")]/ul/li/div/span[contains(@class, "u-menu_a")]')
                if len(res) > 0:
                    #succes add
                    if res[0].text == u"Запрос отправлен":
                        return INV_OK
                else:
                    return INV_ERROR
        else:
            # Alredy voted
            return INV_ALREADY

    def send_message(self, msg_text):
        sleep(3)
        self.center_click(self.driver.find_element_by_id("action_menu_write_message_a"))
        sleep(5)
        elem = self.driver.find_elements(By.XPATH,
           u".//div[@id='msg_layer_wrapper']//form/div[@class='comments_add-itx']//div[starts-with(@id, 'field_txt')]")
        elem[0].send_keys(unicode(msg_text, 'utf-8'))
        sleep(5)
        elem = self.driver.find_elements(By.XPATH, u"//button[contains(@class, 'comments_add-controls_save')]")[0]
        self.center_click(elem)
        return 0

    def center_click(self, obj):
        y = self.driver.execute_script("return window.scrollY;")
        h = self.driver.get_window_size()['height'] / 2
        scroll_y = max(obj.location['y'] - h, 0)
        self.driver.execute_script("window.scrollTo(0, {0} );".format(scroll_y))
        sleep(3)
        obj.click()

    def center_scroll(self, obj):
        y = self.driver.execute_script("return window.scrollY;")
        h = self.driver.get_window_size()['height'] / 2
        scroll_y = max(obj.location['y'] - h, 0)
        self.driver.execute_script("window.scrollTo(0, {0} );".format(scroll_y))

    def fill_filter_old(self, gender = None, from_age = None, till_age = None, location = None, on_site = None,
                        walk_plan = None, url = None):

        self.driver.set_page_load_timeout(50)
        try:
            self.driver.get(url)
            #w = self.driver.get_window_size()['width']
            #self.driver.set_window_size(w, 640)
        except:
            r = 1

        sex_tag = 'span'
        # изменение от 15.12.2016
        sex_tag = 'div'

        # переход в начало страницы
        self.driver.execute_script("window.scrollTo(0, 20);")
        sleep(3)
        flts = self.driver.find_elements_by_class_name("gs_filter_list")
        if gender is not None:
            lst = flts[0].find_elements_by_tag_name('li')
            if gender == 'm':
                lst[1].find_element_by_tag_name(sex_tag).click()
            if gender == 'f':
                lst[2].find_element_by_tag_name(sex_tag).click()

        if from_age is not None:
            elem = Select(flts[1].find_elements_by_tag_name('select')[0])
            elem.select_by_value(from_age)
            #elem = flts[1].find_elements_by_tag_name('select')[0].find_element_by_xpath("//option[@value='"+from_age+"']")
            #elem.click()

        if till_age is not None:
            elem = Select(flts[1].find_elements_by_tag_name('select')[1])
            elem.select_by_value(till_age)
            #elem = elem.find_element_by_xpath("option[@value='" + till_age + "']")
            #elem.click()

        if location is not None:
            i = 0
            while i < 3:
                try:
                    # до 15.12.2016 был тэг спан
                    elem = flts[2].find_element_by_xpath("li/div[@data-field_location='" + location +
                                                         "' and @data-field_country='10414533690']")
                    self.center_click(elem)
                    break
                except:
                    self.driver.execute_script("window.scrollTo(0, 20);")
                    i += 1
            if i >= 3:
                # до 15.12.2016 был тэг спан
                elem = flts[2].find_element_by_xpath("li/div[@data-field_location='" + location +
                                                     "' and @data-field_country='10414533690']")
                elem.click()

        if on_site is not None:
            wait = WebDriverWait(self.driver, 50)
            #elem = wait.until(EC.element_to_be_clickable((By.ID, 'field_onSite')))
            elem = flts[9].find_element_by_id('field_onSite')
            elem_m = flts[9].find_element_by_id('field_refs')
            #elem = WebDriverWait(self.driver, 60).until((EC.visibility_of_element_located(By.ID, 'field_onSite')))
            #elem = wait.until(EC.element_to_be_clickable((By.ID, 'field_onSite')))
            elem = wait.until(EC.visibility_of_element_located((By.ID, 'field_onSite')))
            if on_site != elem.is_selected():
                #action = ActionChains(self.driver)
                #action.move_to_element(elem_m)
                #action.click(elem)
                #action.perform()
                #elem = wait.until(EC.element_to_be_clickable((By.ID, 'field_onSite')))
                elem.click()
                #wait.until(stalenessOf(load));
                #self.driver.move_to_element(elem)
            #print elem.get_attribute('outerHTML')
            #if on_site != elem.is_selected():
            #    elem.click()

        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        self.logger.write_log(WALKER_FIENDS,
                              0,
                              self.logger.dumps(
                                          {'gender': gender,
                                           'from_age': from_age,
                                           'till_age': till_age,
                                           'location': location,
                                           'on_site': on_site,
                                           'walk_plan': walk_plan}),
                                  '')


    # Закрытие вкладок кроме opened первых
    def close_last_windows(self, opened = 1):
        for w in self.driver.window_handles[opened:]:
            self.driver.switch_to_window(w)
            self.driver.close();
            self.driver.switch_to_window(self.driver.window_handles[0])

    # user - обертка пользователя со страницы поиска
    # main_window - handle главного окна (список поиска)
    # try_cnt - количество попыток нажатия добавить в друья
    def add_to_friend(self, user, html_user, main_window, try_cnt):
        handle = self.open_new_tab_user_link(user, html_user, main_window)
        try:
            sleep(3)
            # Несколько попыток нажать кнопку добавить в друзья
            for i in (0, try_cnt):
                add_res = self.send_invite()
                if add_res < 0:
                    self.close_last_windows()
                    self.open_new_tab_user_link(user, main_window)
                    sleep(3)
                else:
                    break

            if add_res == INV_OK:
                # Проверка ставить ли класс
                if random() < self.class_prob:
                    user['p3'] = self.avatar_class() + 1
                else:
                    user['p3'] = 0
                # Проверка ставить ли оценку
                if random() < self.vote_prob:
                    user['p4'] = self.avatar_vote() + 1
                else:
                    user['p4'] = 0
                # Проверка посылать ли сообщение
                if random() < self.message_prob:
                    user['p5'] = self.select_message(self.add_friend_set_id)
                else:
                    user['p5'] = 0
        except Exception as err:
            self.logger.write_execption(WALKER_FIENDS, err, '')
        finally:
            self.close_tab(handle, main_window)
        return add_res

    def parse_user_params(self, user):
        item = {}
        item['p1'] = None
        item['p2'] = None
        item['p3'] = None
        item['p4'] = None
        item['p5'] = None
        # Получение id поользователя
        x_tmp = user.find_element(By.XPATH,
                               './/div[contains(@class, "gs_result_i_t")]//div[contains(@class, "ellip")]/a')
        item['id'] = int(x_tmp.get_attribute('data-l').split(',')[11])
        # Определение текущего статуса пользователя
        # Наличие кнопки добавить в друзья
        if len(user.find_elements(By.XPATH,'.//div[starts-with(@id, "hook_Block_PS_User_")]/a[contains(@href, "cmd=AddFriendButton")]/span')) > 0:
            item['rel'] = REL_COMMON
            # Получаем атрибуты друга
            # photo count
            x_tmp = user.find_elements(By.XPATH, './/div[contains(@class, "gs_result_i_photos")]/a[@class="al"]')
            if len(x_tmp) > 0:
                item['p1'] = x_tmp[0].text.split(u' ')[-1]
                # common fiends
            x_tmp = user.find_elements(By.XPATH, './/div[@class = "card-list-sm_hld"]/span/a')
            if len(x_tmp) > 0:
                item['p2'] = x_tmp[0].text.split(u' ')[0]
        # Наличие сообщение об отправки приглашения
        elif (len(user.find_elements(By.XPATH,'.//div[starts-with(@id, "hook_Block_PS_User_")]/span[contains(@class, "lstp-t")]')) > 0) or\
             (len(user.find_elements(By.XPATH, './/div[contains(@class, "gs_result_i")]/div/div[contains(@class, "lstp-t")]')) > 0):
            item['rel'] = REL_INVITE
        # Наличие признака Друг
        elif len(user.find_elements(By.XPATH,'.//div[contains(@class, "gs_result_i")]//span[@data-aid="LS_Relation"]')) > 0:
            item['rel'] = REL_FRIEND

        return  item

    def scroll_user_list(self):
        # поиск кнопки "Показать еще"
        show_more = self.driver.find_elements(By.XPATH, self.xpath_show_more)
        if len(show_more) > 0:
            sleep(2)
            show_more.click()

    # Возвразает 2 значения
    #   - количество добавленных элементов
    #   - признак достижения лимита добавлений
    def find_user_list(self, gender = None, from_age = None, till_age = None, location = None, on_site = None,
                       walk_plan = 30, add_to_friends = 0, url = OK_FRIENDS_FILTER_URL):
        # Формирование запроса
        #url = 'https://ok.ru/search?st.mode=Users&st.vpl.mini=false&st.grmode=Groups&st.posted=set'

        self.logger.start_event()
        self.logger.write_log(WALKER_START_FIENDS, 0, 'Start', '')
        limit_stop = False

        try:
            parser = etree.HTMLParser()

            us_friends = []
            us_invated = []
            us_goto = []
            us_send_invate = []
            last_user = 0
            page_down_cnt = 0
            page_down_max_cnt = 15
            try_cnt = 5
            inv_cnt = 0
            self.fill_filter(gender, from_age, till_age, location, on_site, walk_plan, url)

            run = True

            while run:
                # получение списка пользователей
                #users_dom = etree.parse(StringIO(self.driver.find_element(By.XPATH, "//div[@id = 'gs_result_list']").get_attribute('outerHTML')),
                #                              parser)
                rel_date = datetime.datetime.now()
                #users = users_dom.xpath('//body/div/div')
                users = self.driver.find_elements(By.XPATH, "//div[@id = 'gs_result_list']//div[contains(@class, 'gs_result_i_w')]")

                # get user id list
                if len(users) == last_user:
                    if page_down_cnt >= page_down_max_cnt:
                        break
                    else:
                        page_down_cnt += 1

                for x in users[last_user:]:
                    last_user +=1
                    #if last_user % 2 == 0:
                    # Скролл каждые два пользователя
                    self.center_scroll(x)
                    item = {}
                    # Получение id пользователя
                    x_tmp = x.find_element(By.XPATH,
                                           './/div[contains(@class, "gs_result_i_t")]//div[contains(@class, "ellip")]/a')
                    item['id'] = int(x_tmp.get_attribute('data-l').split(',')[11])
                    last_rel = self.get_last_status(item['id'])
                    add_res = 0
                    # Проверка наличия кнопки добавить в друзья
                    if (last_rel is None or last_rel <> REL_FRIEND_OUT) and \
                       (len(x.find_elements(By.XPATH,'.//div[starts-with(@id, "hook_Block_PS_User_")]/a[contains(@href, "cmd=AddFriendButton")]/span')) > 0):
                        # Получаем атрибуты друга
                        # photo count
                        x_tmp = x.find_elements(By.XPATH, './/div[contains(@class, "gs_result_i_photos")]/a[@class="al"]')
                        if len(x_tmp) > 0:
                            item['p1'] = x_tmp[0].text.split(u' ')[-1]
                        else:
                            item['p1'] = None
                            # common fiends
                        x_tmp = x.find_elements(By.XPATH, './/div[@class = "card-list-sm_hld"]/span/a')
                        if len(x_tmp) > 0:
                            item['p2'] = x_tmp[0].text.split(u' ')[0]
                        else:
                            item['p2'] = None
                        item['p3'] = None
                        item['p4'] = None
                        item['p5'] = None
                        item['rel'] = REL_FRIEND
                        add_res = self.add_to_friend(item, self.driver.current_window_handle, try_cnt)
                        if add_res == INV_OK:
                            self.add_users_rel([item], rel_date)
                            inv_cnt = inv_cnt + 1
                        elif add_res == INV_TEMPORARY_CANNONT:
                            run = False
                            limit_stop = True
                            break
                    else:
                        # Проверка наличия вылсанного приглашения

                        if (len(x.find_elements(By.XPATH,'.//div[starts-with(@id, "hook_Block_PS_User_")]/span[contains(@class, "lstp-t")]')) > 0) or\
                            (len(x.find_elements(By.XPATH,
                                                 './/div[contains(@class, "gs_result_i")]/div/div[contains(@class, "lstp-t")]')) > 0):
                            # Приглашение выслано
                            item['rel'] = REL_INVITE
                        elif len(x.find_elements(By.XPATH,'.//div[contains(@class, "gs_result_i")]//span[@data-aid="LS_Relation"]')) > 0:
                            # Уже в друзьях
                            item['rel'] = REL_FRIEND
                        if (last_rel is None) or (last_rel <> item['rel']):
                            item['p1'] = None
                            item['p2'] = None
                            item['p3'] = None
                            item['p4'] = None
                            item['p5'] = None
                            self.add_users_rel([item], rel_date)
                if inv_cnt >= walk_plan:
                    run = False
                    limit_stop = True
                    break

            self.log_friend_list_end(len(us_goto), add_to_friends)
        except Exception as err:
            self.logger.write_execption(WALKER_FIENDS, err, '')
            self.close_last_windows()
        else:
            # close all windows except first
            print sys.exc_info()
            self.close_last_windows()

        return inv_cnt, add_to_friends, limit_stop

    def goto_main_page(self):
        logo = self.driver.find_element(By.XPATH, "//a[@id = 'toolbar_logo_id']")
        logo.click()
        sleep(5)

    def post_status(self, status_text):
        self.goto_main_page()
        status_wrapper = self.driver.find_element(By.XPATH, "//div[@id = 'hook_Block_PostingForm']//div[@class = 'input_placeholder']")
        status_wrapper.click()
        #status_input = self.driver.find_element(By.XPATH, "//div[@id = 'hook_Block_MediaTopicLayerBody']//div[@class = 'posting_itx-w']//div[@data-module='postingForm/mediaText']/div")
        #status_input = self.driver.find_element(By.XPATH, "//div[@id = 'hook_Block_MediaTopicLayerBody']//div[@class = 'posting_itx-w']//div[@class='input_placeholder']")
        #status_input.click()
        actions = ActionChains(self.driver)
        sleep(5)
        actions.send_keys(unicode(status_text, 'utf-8'))
        actions.perform()
        # Флаг установить статус
        inp_status = self.driver.find_element(By.XPATH, "//div[@class = 'posting_f_l']//span[@class = 'irc-vis']")
        inp_status.click()
        # кнопка отправить
        btn_submit = self.driver.find_element(By.XPATH, "//div[@class = 'posting_f_r']/div[@data-action = 'submit']")
        btn_submit.click()
        #status_input.send_keys(unicode(status_text, 'utf-8'))

        return 0