# -*- coding: utf-8 -*-
from okwalker import OkWalker
from db_connect import get_db_connect

import ok_api

def main():
    api = ok_api.OdnoklassnikiRu()

    api.getDefAuth()
    total_header, total_frnd = api.getFriends()


    print total_header
    print total_frnd


#    db = get_db_connect()
#    w = OkWalker(db, '89106455257', 3)
#    w.login()
    #w.open_user_page(517163985946)
    #w.open_user_page(547624660446)
    #w.open_user_page(569377371243)
    #w.open_user_page(538874606576)
#    w.open_user_page(564116456518)
    #print w.avatar_class()
    #print w.avatar_vote()
#    print w.send_invite()
    r = 1
main()