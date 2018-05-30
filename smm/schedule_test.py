# -*- coding: utf-8 -*-

import auto_post
import ok_api
import db_connect
from datetime import date
from datetime import timedelta

ok = ok_api.OdnoklassnikiRu()
db = db_connect.get_db_connect_prod()
#db = db_connect.get_db_connect()

poster = auto_post.Poster(ok, db)
ok.getDefAuth()

st_d = date(2016, 10, 31)

print st_d + timedelta(days=20)

g_uid = 53985143554283

poster.create_promo_schedule(st_d, st_d + timedelta(days=15), uid = 574248559595, gid = g_uid)
poster.post_by_schedule(uid = 574248559595, gid = g_uid)




