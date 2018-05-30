# -*- coding: utf-8 -*-
import db_connect
from random import random
from random import randint
from datetime import timedelta
from datetime import datetime


PROMO_THEME_ID = 1
LAWYER_IMG = 1
TEXTS_COUNT = 9

shift_width = 30


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return long((dt - epoch).total_seconds() * 1000)


class Poster(object):
    def __init__(self, net, db):
        self.net = net
        self.db = db

    def random_row(self, d, ind):
        return d[randint(0, len(d) - 1)][ind]

    def random_rows(self, d, inds, cnt):
        r = []
        d_i = [[x[y] for y in inds] for x in d]
        for x in range(cnt):
            t = self.random_row_all(d_i, inds)
            r.append(t)
            d_i.remove(t)
        return r

    def random_row_all(self, d, inds):
        a = d[randint(0, len(d) - 1)]
        return [a[x] for x in inds]

    def random_images(self, theme_id, cnt):
        sql = 'select i.topic_image_id' \
              '  from social.topic_images i ' \
              ' where i.theme_id = %(theme_id)s '
        img = self.db.do_query_all_params(sql, {'theme_id': theme_id})
        if len(img) > 0:
            return self.random_rows(img, [0], cnt)
        else:
            return []

    def plan_promo(self, d, txt_set, uid, gid, theme_img_p = 1.0, lawer_img_p = 1.0, lawer_img_cnt = 2):
        #Проверка есть ли уже запланированный пост
        sql = "select count(*) as cnt " \
              "  from social.topic_schedule s " \
              " inner join social.topic_texts t on t.topic_text_id = s.topic_text_id " \
              " inner join social.topic_themes tt on tt.theme_id = t.theme_id " \
              " where tt.type_id = %(type_id)s " \
              "   and date_trunc('day', s.schedule_date) = %(date)s "

        if self.db.do_query_one_params(sql, {'type_id': PROMO_THEME_ID, 'date': d})[0] == 0:
#        if self.db.do_query_one_params(sql, {})[0] == 0:
            #Выбор времени публикации
            sql_slot = "select l.slot_id, l.time_value " \
                       "  from social.time_slot l " \
                       " where l.slot_id not in (select slot_id " \
                       "                           from social.topic_schedule s " \
                       "                          where date_trunc('day', s.schedule_date) = %(date)s ) "
            free_slots = self.db.do_query_all_params(sql_slot, {'date': d})
            #выбор случайного значения
            slot = self.random_row_all(free_slots, [0, 1])

            #Случайный выбор текста
            if len(txt_set) == 0:
                sql_texts = 'select t.topic_text_id, t.theme_id ' \
                            '  from social.topic_texts t' \
                            ' inner join social.topic_themes tt on tt.theme_id = t.theme_id ' \
                            ' where tt.type_id = %(type_id)s '
                texts = self.db.do_query_all_params(sql_texts, {'type_id': PROMO_THEME_ID})
                txt_set += self.random_rows(texts, [0, 1], TEXTS_COUNT)

            text_ids = self.random_row_all(txt_set, [0, 1])
            txt_set.remove(text_ids)

            imgs = []

            #Проверка нужно ли добавлять фото услуги
            if (LAWYER_IMG <> text_ids[1]) and (random() < theme_img_p):
                img = self.random_images(text_ids[1], 1)
                imgs += img

            #Проверка нужно ли добавлять фото юристов
            if random() < lawer_img_p:
                img = self.random_images(LAWYER_IMG, lawer_img_cnt)
                imgs += img

            # добавление новой записи в график
            sql_insert = "insert into social.topic_schedule(schedule_id, " \
                         "  topic_text_id, " \
                         "  user_id, " \
                         "  group_id, " \
                         "  slot_id, " \
                         "  schedule_date, " \
                         "  is_posted) " \
                         "values (nextval('social.seq_topic_schedule'), " \
                         "  %(topic_text_id)s, " \
                         "  %(user_id)s, " \
                         "  %(group_id)s, " \
                         "  %(slot_id)s, " \
                         "  %(schedule_date)s, " \
                         "  0)" \
                         "returning schedule_id"

            rmin = randint(-10, 15)
            td = datetime.combine(d, slot[1]) + timedelta(minutes = rmin)

            sch_id = self.db.do_query_one_params(sql_insert, {'topic_text_id': text_ids[0], 'slot_id': slot[0],
                                                              'user_id': uid, 'group_id': gid,
                                                              'schedule_date': td})[0]

            sql_insert_img = 'insert into social.topic_schedule_img values (%(schedule_id)s, %(ord)s, %(topic_image_id)s)'
            i = 0
            for x in imgs:
                self.db.exec_query_params(sql_insert_img, {'schedule_id': sch_id, 'ord': i, 'topic_image_id': x[0]})
                i += 1
        return 0


    def create_promo_schedule(self, from_date, to_date, uid, gid):
        t = []
        for d in range(int((to_date - from_date).days)):
            self.plan_promo(from_date + timedelta(d), t, uid, gid)
        self.db.exec_query('commit;')
        return 0

    def post_scheduled_topic(self, schedule_id):
        sql = 'select s.group_id, t.topic_caption, t.topic_text, s.schedule_date ' \
              '  from social.topic_schedule s ' \
              ' inner join social.topic_texts t on t.topic_text_id = s.topic_text_id ' \
              ' where s.schedule_id = %(schedule_id)s '
        topic = self.db.do_query_one_params(sql, {'schedule_id': schedule_id})

        img_sql = 'select i.img, i.topic_image_id' \
                  '  from social.topic_schedule_img t ' \
                  ' inner join social.topic_images i on i.topic_image_id = t.topic_image_id ' \
                  ' where t.schedule_id = %(schedule_id)s ' \
                  ' order by t.ord '

        img_b = []
        for x in self.db.do_query_all_params(img_sql, {'schedule_id': schedule_id}):
            img_b.append(x[0])

        resp, dis = self.net.postToGroup(topic[0], topic[1] + '\n' + topic[2], img_buf=img_b,
                                         post_at = unix_time_millis(topic[3]))

        update_sql = 'update social.topic_schedule' \
                     '   set is_posted = 1,' \
                     '       posted_topic_id = %(topic_id)s ' \
                     ' where schedule_id = %(schedule_id)s'

        if resp['status'] == '200':
            self.db.exec_query_params(update_sql, {'topic_id': long(dis), 'schedule_id': schedule_id})

        return 0

    def post_by_schedule(self, uid, gid):
        sql = 'select schedule_id, ' \
              '       topic_text_id, ' \
              '       user_id, ' \
              '       group_id, ' \
              '       slot_id, ' \
              '       schedule_date ' \
              '  from social.topic_schedule t ' \
              ' where t.is_posted = 0 ' \
              '   and t.user_id = %(user_id)s ' \
              '   and t.group_id = %(group_id)s ' \
              ' order by schedule_date'
        topics = self.db.do_query_all_params(sql, {'user_id': uid, 'group_id': gid})

        for x in topics:
            self.post_scheduled_topic(x[0])
        return 0

