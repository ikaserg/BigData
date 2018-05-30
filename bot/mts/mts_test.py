import call_report
import datetime

def main():
    rep = call_report.MtsReport({'login': '(915) 598-92-07',
                                 'password': '6wiqNt',
                                 'email': 'mts@ikaserg.ru',
                                 'from_date': datetime.date(2016, 11, 1),
                                 'to_date': datetime.date(2016, 11, 2)})
    rep.call_report()
    None
main()