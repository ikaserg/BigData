# -*- coding: utf-8 -*-
import db_connect
import ok_api
from social_consts import LIST_USER_LOGON
from iter_file import IteratorFile

from datetime import datetime

class OkServices():
    def __init__(self, api, db):
        self.api = api
        self.db = db
        self.fields = 'first_name,last_name,gender,birthday,location,current_status,' \
                      'current_status_id,current_status_date,url_profile,allows_anonym_access,' \
                      'registered_date,premium'

    def addNewFriends(self):
        sql = 'insert into social.users(social_net_id, user_id, create_date) ' \
              '     select r.social_net_id, r.rel_user_id, now() ' \
              '       from social.user_relations r ' \
              '      where r.social_net_id = %(social_net_id)s ' \
              '        and (r.social_net_id, r.rel_user_id) not in ' \
              '              (select u_i.social_net_id, u_i.user_id ' \
              '                 from social.users u_i) ' \
              '        and r.relation_type_id in (1, 4)' \
              '      group by r.social_net_id, r.rel_user_id'
        self.db.exec_query_params(sql, {'social_net_id': self.api.social_id})
        self.db.exec_query('commit')
        return 0


    def collectNewInfo(self, wnd = 100):
        sql = 'select u.user_id from social.users u where u.url_profile is null and u.is_deleted is null'
        uids = [x[0] for x in  self.db.do_query_all(sql)]

        uid_cnt = len(uids)
        x = 0
        while x < uid_cnt:
            l = min(wnd, uid_cnt - x)
            r, ui = self.api.getUsersInfo(uids[x: x+l], self.fields)
            self.updateUserInfo(ui)
            x += l

    def val(self, dict, key):
        if dict is None:
            return None
        else:
            if key in dict:
                return dict[key]
            else:
                return None

    def xstr(self, x):
        return '' if x is None else x

    def extract_birthday(self, ui, name = 'birthday'):
        b = self.xstr(self.val(ui, name))
        return b[:10] if len(b) > 5 else None

    def extract_birth_day(self, ui, name = 'birthday'):
        b = self.val(ui, name)
        return None if b is None else b[-2:]

    def extract_birth_month(self, ui, name = 'birthday'):
        b = self.val(ui, name)
        return None if b is None else b[-5:-3]

    def extract_fullname(self, ui, first_name = 'first_name', last_name = 'last_name'):
        fn = self.val(ui, first_name)
        ln = self.val(ui, last_name)
        return ' '.join([self.xstr(fn), self.xstr(ln)])

    def appendMsgUsers(self):
        sql = 'select user_id ' \
              'from( ' \
              'select m.from_user_id as user_id' \
              '  from social.messages m ' \
              ' where m.from_user_id not in (select ui.user_id ' \
              '                                from social.users ui ' \
              '                               where ui.social_net_id = %(social_net_id)s ) ' \
              '   and m.social_net_id = %(social_net_id)s '\
              'union ' \
              'select m.to_user_id ' \
              '  from social.messages m ' \
              ' where m.to_user_id not in (select ui.user_id ' \
              '                              from social.users ui ' \
              '                             where ui.social_net_id = %(social_net_id)s ) '\
              '   and m.social_net_id = %(social_net_id)s ' \
              ') t ' \
              'group by user_id'

        self.handleUsersSql(sql, self.insertUsers)

    def handleUsersSql(self, sql, handler, wnd = 100):
        # Получение списка id пользователей
        uids = self.db.do_query_all_params(sql, {'social_net_id': self.api.social_id})

        # Обработка полученного списка с окном не более wnd
        uid_cnt = len(uids)
        x = 0
        while x < uid_cnt:
            l = min(wnd, uid_cnt - x)
            # Получение информации о пользователях
            r, ui = self.api.getUsersInfo([i[0] for i in uids[x: l]], self.fields)

            # Вызов обработчика
            handler(ui)
            x = x + l
        return 0


    def insertUsers(self, u_info):
        sql = 'insert into social.users(  ' \
              '      social_net_id, ' \
              '      user_id, ' \
              '      name, '\
              '      first_name, '\
              '      last_name, '\
              '      gender, '\
              '      birthday, '\
              '      birth_day, '\
              '      birth_month, '\
              '      city, '\
              '      country, '\
              '      current_status, '\
              '      current_status_id, '\
              '      current_status_date, '\
              '      url_profile, '\
              '      allows_anonym_access, '\
              '      registered_date, '\
              '      premium, '\
              '      create_date, ' \
              '      update_date ' \
              ') ' \
              'values(' \
              '      %(social_net_id)s, ' \
              '      %(user_id)s, ' \
              '      %(name)s, '\
              '      %(first_name)s, '\
              '      %(last_name)s, '\
              '      %(gender)s, '\
              '      %(birthday)s, '\
              '      %(birth_day)s, '\
              '      %(birth_month)s, '\
              '      %(city)s, '\
              '      %(country)s, '\
              '      %(current_status)s, '\
              '      %(current_status_id)s, '\
              '      %(current_status_date)s, '\
              '      %(url_profile)s, '\
              '      %(allows_anonym_access)s, '\
              '      %(registered_date)s, '\
              '      %(premium)s, '\
              '      now(), ' \
              '      now() ' \
              ')' \

        for x in u_info:
            #try:
            self.db.exec_query_params(sql,
                                      {'name': self.extract_fullname(x),
                                       'first_name': self.val(x, 'first_name'),
                                       'last_name': self.val(x, 'last_name'),
                                       'gender': 1 if self.val(x, 'gender') == 'male' else 2,
                                       'birthday': self.extract_birthday(x),
                                       'birth_day': self.extract_birth_day(x),
                                       'birth_month': self.extract_birth_month(x),
                                       'city': self.val(self.val(x, 'location'), 'city'),
                                       'country': self.val(self.val(x, 'location'), 'countryName'),
                                       'current_status': self.val(x, 'current_status'),
                                       'current_status_id': self.val(x, 'current_status_id'),
                                       'current_status_date': self.val(x, 'current_status_date'),
                                       'url_profile': self.val(x, 'url_profile'),
                                       'allows_anonym_access': 1 if self.val(x, 'allows_anonym_access') == 'true' else 0,
                                       'registered_date': self.val(x, 'registered_date'),
                                       'premium': 1 if self.val(x, 'premium') == 'true' else 0,
                                       'social_net_id': self.api.social_id,
                                       'user_id': self.val(x, 'uid')})
        self.db.exec_query('commit')


    def updateUserInfo(self, u_info):
        sql = 'update social.users set ' \
              '      name = %(name)s, '\
              '      first_name = %(first_name)s, '\
              '      last_name = %(last_name)s, '\
              '      gender = %(gender)s, '\
              '      birthday = %(birthday)s, '\
              '      birth_day = %(birth_day)s, '\
              '      birth_month = %(birth_month)s, '\
              '      city = %(city)s, '\
              '      country = %(country)s, '\
              '      current_status = %(current_status)s, '\
              '      current_status_id = %(current_status_id)s, '\
              '      current_status_date = %(current_status_date)s, '\
              '      url_profile = %(url_profile)s, '\
              '      allows_anonym_access = %(allows_anonym_access)s, '\
              '      registered_date = %(registered_date)s, '\
              '      premium = %(premium)s, '\
              '      update_date = now() ' \
              ' where social_net_id  = %(social_net_id)s '\
              '   and user_id = %(user_id)s '\

        for x in u_info:
            #try:
            self.db.exec_query_params(sql,
                                      {'name': self.extract_fullname(x),
                                       'first_name': self.val(x, 'first_name'),
                                       'last_name': self.val(x, 'last_name'),
                                       'gender': 1 if self.val(x, 'gender') == 'male' else 2,
                                       'birthday': self.extract_birthday(x),
                                       'birth_day': self.extract_birth_day(x),
                                       'birth_month': self.extract_birth_month(x),
                                       'city': self.val(self.val(x, 'location'), 'city'),
                                       'country': self.val(self.val(x, 'location'), 'countryName'),
                                       'current_status': self.val(x, 'current_status'),
                                       'current_status_id': self.val(x, 'current_status_id'),
                                       'current_status_date': self.val(x, 'current_status_date'),
                                       'url_profile': self.val(x, 'url_profile'),
                                       'allows_anonym_access': 1 if self.val(x, 'allows_anonym_access') == 'true' else 0,
                                       'registered_date': self.val(x, 'registered_date'),
                                       'premium': 1 if self.val(x, 'premium') == 'true' else 0,
                                       'social_net_id': self.api.social_id, 'user_id': self.val(x, 'uid')})
            #except:
            #    print 'error'
            #    print self.val(x, 'birthday')
            #    print self.extract_birth_day(x)
            #    print self.extract_birth_month(x)
            #    print self.val(x, 'uid')

        self.db.exec_query('commit')
        return 0

    def insertUsersInfo(self, wnd = 100):
        sql = 'select r.social_net_id, r.rel_user_id ' \
              '  from social.user_relations r ' \
              ' where r.social_net_id = %(social_net_id)s ' \
              '   and (r.social_net_id, r.rel_user_id) not in ' \
              '         (select u_i.social_net_id, u_i.user_id ' \
              '            from social.users u_i) '

        insert_user_info = 'insert into social.users() '

        uids = self.db.do_query_all(sql, {'social_net_id': self.api.social_id})

        uid_cnt = len(uids)
        x = 0

        while x < uid_cnt:
            l = min(wnd, uid_cnt - x)
            r, ui = self.api.getUsersInfo(uids[x, l], self.fields)
            for i in ui:
                None


    def collectUsersInfo(self, uids):
        # Выбор друзей у которых нет ссылки на профиль
        return 0

    def process_user_status_list(self, lst_ol, lst_out):
        empty_temp_user_state = 'delete from social.temp_users_last_state;'

        insert_user_logon = 'insert into social.users_login(social_net_id, user_id, login_date, online_status)' \
                            ' select t_s.social_net_id, t_s.user_id, now(), t_s.online_status' \
                            '   from social.temp_users_last_state t_s' \
                            '  inner join social.users_last_state s on s.social_net_id = t_s.social_net_id' \
                            '                                     and s.user_id =  t_s.user_id' \
                            '                                     and s.online_status <> t_s.online_status'

        update_user_state = 'update social.users_last_state t' \
                            '   set online_status = t_s.online_status, state_date = now() '\
                            '  from social.temp_users_last_state t_s ' \
                            '   where t.social_net_id = t_s.social_net_id '\
                            '     and t.user_id =  t_s.user_id' \
                            '     and exists (select 1 ' \
                            '                   from social.users_last_state s ' \
                            '                  where s.social_net_id = t_s.social_net_id '\
                            '                    and s.user_id =  t_s.user_id ' \
                            '                    and s.online_status <> t_s.online_status); ' \

        insert_user_state = 'insert into social.users_last_state(social_net_id, user_id, online_status ,state_date) ' \
                            ' select t_s.social_net_id, t_s.user_id, t_s.online_status, now()' \
                            '   from social.temp_users_last_state t_s' \
                            '  where not exists(select 1 ' \
                            '                     from social.users_last_state s ' \
                            '                    where s.social_net_id = t_s.social_net_id ' \
                            '                      and s.user_id =  t_s.user_id) ' \

        # Очистка временной таблицы
        self.db.exec_query(empty_temp_user_state)

        f = IteratorFile((u'{}\t{}\t{}'.format(self.api.social_id, x, 1) for x in lst_ol))
        self.db.copy_from_file(f, 'social.temp_users_last_state', ('social_net_id', 'user_id', 'online_status'))

        f = IteratorFile((u'{}\t{}\t{}'.format(self.api.social_id, x, -1) for x in lst_out))
        self.db.copy_from_file(f, 'social.temp_users_last_state', ('social_net_id', 'user_id', 'online_status'))

        self.db.exec_query(insert_user_logon)
        self.db.exec_query(update_user_state)
        self.db.exec_query(insert_user_state)

        self.db.exec_query('commit')
        return 0

    def collect_online_users(self):
        # Получаем список пользователей

        user_sql = 'select ua.user_id, ua.token, ua.session_secret, sa.action_type' \
                   '  from schedule.scheduled_action sa' \
                   ' inner join social.users_auth ua on ua.social_net_id = sa.social_net_id' \
                   '                                and ua.user_id = sa.user_id' \
                   ' where sa.social_net_id = 3' \
                   ' order by ua.user_id'

        insert_sql = "insert into social_stat.friends_online_stat " \
                     "values('{0}', '{1}', to_timestamp('{2}', 'DD Mon YYYY HH24:MI:SS'), '{3}', '{4}')"

        crt_temp_user_list = 'create temporary table handled_users( ' \
                             'social_net_id integer, ' \
                             'user_id bigint ' \
                             ') ' \
                             'on commit delete rows;' \
                             'create index temp_1 on temp_user_list_item(social_net_id, user_id);'
        empty_temp_user_list = 'delete from social.temp_user_list_item;'

        insert_user_list = 'insert into social.user_list_item(user_list_id, social_net_id, user_id, add_date)' \
                           'select user_list_id, social_net_id, user_id, now()' \
                           '  from social.temp_user_list_item'

        user_list = 'insert into social.user_list_item(user_lists_id, social_net_id, user_id, add_date)' \
                    'values (%(user_lists_id)s, %(social_net_id)s, %(user_id)s, %(add_date)s)'

        clear_user_list = 'delete from social.temp_user_list_item t ' \
                          '      where EXISTS (select 1 ' \
                          '                      from social.user_list_item  l ' \
                          '                     where l.social_net_id = t.social_net_id' \
                          '                       and l.user_id = t.user_id)'

        insert_new_friends1 = 'insert into social.user_relations(social_net_id, user_id, rel_user_id, relation_date, ' \
                              '                                  relation_type_id) ' \
                              'select t.social_net_id, %(user_id)s, t.user_id, %(relation_date)s, %(relation_type_id)s ' \
                              '  from social.temp_user_list_item t ' \
                              ' where not exists (select 1 ' \
                              '                     from social.user_relations r ' \
                              '                    where r.social_net_id = t.social_net_id ' \
                              '                      and r.rel_user_id = t.user_id ' \
                              '                      and r.user_id = %(user_id)s ' \
                              '                      and r.relation_type_id = 1) '

        insert_new_friends = 'insert into social.user_relations(social_net_id, user_id, rel_user_id, relation_date, ' \
                             '                                  relation_type_id) ' \
                             'select t.social_net_id, %(user_id)s, t.user_id, %(relation_date)s, %(relation_type_id)s ' \
                             '  from social.temp_user_list_item t ' \
                             '  left join social.user_relations r on r.social_net_id = t.social_net_id ' \
                             '                                   and r.rel_user_id = t.user_id ' \
                             '                                   and r.user_id = %(user_id)s ' \
                             '                                   and r.relation_date = ' \
                             '                                      (select max(r_m.relation_date) ' \
                             '                                         from social.user_relations r_m ' \
                             '                                        where r_m.social_net_id = r.social_net_id ' \
                             '                                          and r_m.user_id = r.user_id ' \
                             '                                          and r_m.rel_user_id = r.rel_user_id ' \
                             '                                          and r_m.relation_type_id in (1, 5, 6)) ' \
                             ' where coalesce(r.relation_type_id, -1) in (-1, 6) '

        insert_out_friends = 'insert into social.user_relations(social_net_id, user_id, rel_user_id, relation_date, ' \
                             '                                  relation_type_id) ' \
                             'select r.social_net_id, r.user_id, r.rel_user_id, %(relation_date)s, %(relation_type_id)s ' \
                             '  from social.user_relations r ' \
                             ' where r.user_id = %(user_id)s ' \
                             '   and r.relation_date = ' \
                             '         (select max(r_m.relation_date) ' \
                             '            from social.user_relations r_m ' \
                             '           where r_m.social_net_id = r.social_net_id ' \
                             '             and r_m.user_id = r.user_id ' \
                             '             and r_m.rel_user_id = r.rel_user_id ' \
                             '             and r_m.relation_type_id in (1, 5, 6)) ' \
                             '   and r.relation_type_id in (1, 5) ' \
                             '   and not exists (select 1 ' \
                             '                     from social.temp_user_list_item t ' \
                             '                    where t.social_net_id = r.social_net_id ' \
                             '                      and t.user_id = r.rel_user_id )'

        for act in self.db.do_query_all(user_sql):
            if act[3] == 'friends.online':
                # запрос количества друзей
                self.api.token = act[1]
                self.api.session_secret_key = act[2]
                online_header, online_frnd = self.api.getOnlineFriends()
                total_header, total_frnd = self.api.getFriends()

                date_str = online_header['date'].split(', ')[1]
                req_date = datetime.strptime(date_str[:-4], '%d %b %Y %H:%M:%S')

                self.db.exec_query(insert_sql.format(3, act[0], date_str, len(online_frnd), len(total_frnd)))
                self.db.exec_query('commit')

                # Добавление пользователей в список наблюдения
                # db.exec_query(crt_temp_user_list)
                f = IteratorFile((u'{}\t{}\t{}'.format(LIST_USER_LOGON, self.api.social_id, x) for x in total_frnd))
                self.db.copy_from_file(f, 'social.temp_user_list_item', ('user_list_id', 'social_net_id', 'user_id'))
                self.db.exec_query(clear_user_list)
                self.db.exec_query(insert_user_list)
                self.db.exec_query(empty_temp_user_list)
                self.db.exec_query('commit')

                # Получаем список обрабатываемых пользователей
                get_user_list = 'select t.social_net_id, t.user_id ' \
                                '  from social.user_list_item t' \
                                ' where t.user_list_id = %(list)s'

                ul = self.db.do_query_all_params(get_user_list, {'list': LIST_USER_LOGON})
                # Добавление информации о друзьях
                self.process_user_status_list(online_frnd, [x for x in total_frnd if x not in online_frnd])
                # Удаление обработанных пользователей
                ul = [x for x in ul if x not in total_frnd]

                # Добавление друзей в список отношений
                self.db.exec_query(empty_temp_user_list)
                f = IteratorFile((u'{}\t{}\t{}'.format(LIST_USER_LOGON, self.api.social_id, x) for x in total_frnd))
                self.db.copy_from_file(f, 'social.temp_user_list_item', ('user_list_id', 'social_net_id', 'user_id'))
                self.db.exec_query_params(insert_new_friends, {'user_id': act[0], 'relation_date': req_date,
                                                          'relation_type_id': 1})
                self.db.exec_query_params(insert_out_friends, {'user_id': act[0], 'relation_date': req_date,
                                                          'relation_type_id': 6})
                self.db.exec_query('commit')


#def main():
#    # Получаем соединение с БД
#    db = db_connect.get_db_connect_prod()
#
#    # Создаем класс api
#    ok = ok_api.OdnoklassnikiRu()
#    ok.getDefAuth()


#    ok_srv = OkServices(ok, db)

    # Регистрация пользователей online
#    ok_srv.collect_online_users()

    # Сбор информации по пользователям
#    ok_srv.addNewFriends()
#    ok_srv.collectNewInfo()

#    ok.getAndrewAuth()


    # Регистрация пользователей online
#    ok_srv.collect_online_users()

    # Сбор информации по пользователям
#    ok_srv.addNewFriends()
#    ok_srv.collectNewInfo()

#main()

