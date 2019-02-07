from session import SessionManager
from session import DaySession
from db_connect import get_db_connect_prod

def main():
    print 'qwerty'
    db = get_db_connect_prod()
    man = DaySession(db)
    r = man.get_day_session()
    man.set_int_variable('test1', 56)
    man.set_varchar_variable('test2', 'asdfgh')
    print r

main()

