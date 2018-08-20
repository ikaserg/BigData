import psycopg2

class filed_by_names(object):
    def __init__(self, cursor, row):
        for (attr, val) in zip((d[0] for d in cursor.description), row) :
            setattr(self, attr, val)

class db_sql():
    def __ini__(self):
        self.db_connect = None

    def	connect(self, dbname, user, password):
        return 0

    def do_query(self, sql):
        return 0

class db_postgres(db_sql):
    def connect_host(self, host, dbname, user, password):
        self.db_connect = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, dbname, user, password))
        return self.db_connect

    def	connect(self, dbname, user, password):
        self.db_connect = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(dbname, user, password))
        return self.db_connect

    def exec_query(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        return 0

    def commit(self):
        cur = self.db_connect.cursor()
        cur.execute('commit;')
        return 0

    def do_query(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        return cur

    def do_query_one(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def do_query_all(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def do_query_all_fbn(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        return [filed_by_names(cur, x) for x in cur.fetchall()]

    def exec_query_params(self, sql, params, prn=False):
        if prn:
            print sql
            print params
        cur = self.db_connect.cursor()
        cur.execute(sql, params)
        return cur

    def do_query_params(self, sql, params):
        cur = self.db_connect.cursor()
        cur.execute(sql, params)
        return cur

    def do_query_one_params(self, sql, params):
        cur = self.db_connect.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def do_query_all_params(self, sql, params):
        cur = self.db_connect.cursor()
        cur.execute(sql, params)
        if cur.rowcount > 0:
            return cur.fetchall()
        else:
            return [None]


    def do_query_all_fbn_params(self, sql, params):
        cur = self.db_connect.cursor()
        cur.execute(sql, params)
        return [filed_by_names(cur, x) for x in cur.fetchall()]

    def copy_from_file(self, f, table, columns):
        cur = self.db_connect.cursor()
        return cur.copy_from(f, table, columns=columns)
