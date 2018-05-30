# -*- coding: utf-8 -*-
from time import sleep
from okwalker import OkWalker
from db_connect import get_db_connect_prod

from random import randint
from random import random

def main():
    db = get_db_connect_prod()
    w = OkWalker(db, '89106455257')
    w.login()
    t = 0
    w. open_user_page(77820846472)
    w.select_message(1)
    #w.send_message(u'Привет проверка связи')


main()