import sys

sys.path.insert(0, 'E:\Grive\BigData\prod\etl\bot\mts')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl\bot')
sys.path.insert(0, 'E:\Grive\BigData\prod\etl')

import call_report
import datetime
import db_connect

def main():
    db = db_connect.get_db_connect_prod()
    r = call_report.RunReport(call_report.MtsReport, db)
    r.do_report()

main()