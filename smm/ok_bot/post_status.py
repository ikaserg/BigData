# -*- coding: utf-8 -*-
from okwalker import OkWalker
from db_connect import get_db_connect
from time import sleep

def main():
    db = get_db_connect()
    w = OkWalker(db, '89106455257')
    w.login()
    #develop
    w.post_status('Нужен совет опытного юриста? Я решу ваши проблемы! Звоните 8 915 598-92-07')
    sleep(30)
main()