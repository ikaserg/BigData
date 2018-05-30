from json import dumps
import traceback

class Logger(object):
    def __init__(self, db):
        self.db = db

    def start_event(self):
        self.is_event = 1
        self.event_id = self.next_event_id()

    def stop_event(self):
        self.is_event = 0
        self.event_id = None

    def dumps(self, obj):
        return dumps(obj)

class BotLogger(Logger):
    def __init__(self, db, bot_id):
        super(BotLogger, self).__init__(db)
        self.bot_id = bot_id
        self.event_id = None
        self.is_event = 0

    def next_event_id(self):
        sql = "select nextval('social.bot_log_bot_log_id')"
        return self.db.do_query_one(sql)[0]

    def write_log(self, action_id, status, note, error_msg):
        sql = 'insert into  social.bot_log(' \
              ' bot_log_id, ' \
              ' bot_id, ' \
              ' log_date, ' \
              ' action_id, ' \
              ' status,' \
              ' note, ' \
              ' error_msg)' \
              'values(' \
              ' {0}, ' \
              ' %(bot_id)s, ' \
              ' now(), ' \
              ' %(action_id)s, ' \
              ' %(status)s,' \
              ' %(note)s, ' \
              ' %(error_msg)s' \
              ')'
        if self.is_event <> 0 :
            sql = sql.format(str(self.event_id))
        else:
            sql = sql.format("nextval('social.bot_log_bot_log_id')")

        self.db.exec_query_params(sql, {'bot_id': self.bot_id,
                                        'action_id': action_id,
                                        'status': status,
                                        'note': note,
                                        'error_msg': error_msg})
        self.db.commit()


    def write_execption(self, action_id, excep, note = None):
        self.write_log(action_id, -1, '', traceback.format_exc())

