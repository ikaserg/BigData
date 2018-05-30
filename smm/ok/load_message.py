# -*- coding: utf-8 -*-
from okwalker import OkWalker
from db_connect import get_db_connect

def main():
    db = get_db_connect()
    w = OkWalker(db, '89106455257')
    w.login()

    w.load_all_message()

main()