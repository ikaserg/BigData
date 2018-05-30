from selenium import webdriver
import ast
from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

CHROMEDRIVER_PATH = 'D:\Distrib\python\chromedriver_win32\chromedriver.exe'

class GetReport(object):
    def __init__(self, params = None, driver = None):
        #self.params = ast.literal_eval(params)
        self.params = params
        if driver is None:
            self.driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        else:
            self.driver = driver

class MtsReport(GetReport):
    def __init__(self, params = None, driver = None):
        super(MtsReport, self).__init__(params, driver)
        self.login_url = 'https://login.mts.ru/amserver/UI/Login?arg=newsession&goto=http%3A%2F%2Fwww.ryazan.mts.ru%2F'
        self.logout_url = 'https://login.mts.ru/amserver/UI/Logout'
        self.lk_url = 'https://lk.ssl.mts.ru/'
        self.detail_url = 'https://ihelper.mts.ru/selfcare/doc-detail-report.aspx'
        self.source_id = 1

    def login(self):
        self.driver.get(self.login_url)
        frm = self.driver.find_elements(By.XPATH, "//form[@name = 'Login']")[0]
        user_name = frm.find_elements(By.XPATH, "//input[@id = 'phone']")[0]
        user_name.send_keys(self.params['login'])

        psw = frm.find_elements(By.XPATH, "//input[@id = 'password']")[0]
        psw.send_keys(self.params['password'])
        psw.send_keys(Keys.RETURN)
        sleep(3)
        self.driver.get(self.lk_url)
        sleep(3)

        #btn = frm.find_elements(By.XPATH, "//input[contains(@class = 'btn_login']")[0]

    def logout(self):
        self.driver.get(self.logout_url)

    def clear_date(self, elem):
        for i in range(10):
            elem.send_keys(Keys.BACK_SPACE)

    def set_params(self, email, from_date, to_date):
        # step 1
        elem = self.driver.find_elements(By.XPATH, "//input[@name = 'ctl00$MainContent$drp$from']")[0]
        self.clear_date(elem)
        elem.send_keys(from_date.strftime("%d.%m.%Y"))
        elem = self.driver.find_elements(By.XPATH, "//input[@name = 'ctl00$MainContent$drp$to']")[0]
        self.clear_date(elem)
        elem.send_keys(to_date.strftime("%d.%m.%Y"))
        elem = self.driver.find_elements(By.ID, "ctl00_MainContent_btnFirstToSecond")[0]
        elem.send_keys(Keys.RETURN)

        # step 2
        elem = self.driver.find_elements(By.ID, "ctl00_MainContent_dmlMethods_1")[0]
        elem.click()
        elem = self.driver.find_elements(By.XPATH, "//input[@name = 'ctl00$MainContent$dmlMethods$1']")[0]
        elem.send_keys(email)
        self.driver.execute_script("window.scrollTo(0, 200);")
        elem = self.driver.find_elements(By.ID, "ctl00_MainContent_btnSecondToThird")[0]
        elem.click()

        # step 3
        self.driver.execute_script("window.scrollTo(0, 200);")
        elem = self.driver.find_elements(By.ID, "ctl00_MainContent_btnThirdToLast")[0]
        elem.click()

        # step 4
        self.driver.execute_script("window.scrollTo(0, 200);")
        elem = self.driver.find_elements(By.ID, "ctl00_MainContent_btnOrder")[0]
        elem.click()

        return 0

    def get_call_report(self, email, from_date, to_date):
        self.driver.get(self.detail_url)
        self.set_params(email, from_date, to_date)


    def call_report(self):
        self.login()
        self.get_call_report(self.params['email'], self.params['from_date'], self.params['to_date'])

class RunReport(object):
    def __init__(self, report_class, db):
        self.db = db
        self.rep = report_class()
        self.class_name = self.rep.__class__.__name__

    def do_report(self):
        sql = 'select act_period, date_mask, time_mask, bot_class_name, bot_params ' \
              '  from schedule.schedule_bot_action t ' \
              ' where t.bot_class_name = %(class_name)s '

        sql_dates = 'select (t.date_to::date - 1)::date as date_to, t.date_next ' \
                    '  from( ' \
                    '    select coalesce((select min(t_n.date_from) ' \
                    '              from etl.etl_log t_n ' \
                    '             where t_n.source_id = t.source_id ' \
                    '               and t_n.source_key = t.source_key ' \
                    '               and t_n.date_to > t.date_to), now()::date) as date_next, ' \
                    '           t.date_to ' \
                    '      from etl.etl_log t ' \
                    '     where t.source_id = %(source_id)s ' \
                    '       and t.source_key = %(source_key)s ' \
                    '       and t.date_from > %(start_date)s ' \
                    '     group by t.source_id,  t.source_key, t.date_to ' \
                    '      ) t ' \
                    ' where t.date_next::date - t.date_to::date > 0 ' \
                    ' group by t.date_next, t.date_to ' \
                    ' order by t.date_to '

        lgs = self.db.do_query_params(sql, {'class_name': self.class_name})

        for x in lgs:
            self.rep.params = ast.literal_eval(x[4])
            prds = self.db.do_query_params(sql_dates,
                                           {'source_id': self.rep.source_id,
                                            'source_key': self.rep.params['source_key'],
                                            'start_date': datetime.strptime('03052016', '%d%m%Y')})
            self.rep.login()
            for p in prds:
                self.rep.params['from_date'] = p[0]
                self.rep.params['to_date'] = p[1]
                self.rep.get_call_report(self.rep.params['email'],
                                         self.rep.params['from_date'],
                                         self.rep.params['to_date'])
            self.rep.logout()
