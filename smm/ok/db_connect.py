# -*- coding: utf-8 -*-
import db_sql

# Соединение с базой данных
def get_db_connect():
	db = db_sql.db_postgres()
	#db.connect_host('185.154.14.162', 'crm', 'etl', 'etluser')
	db.connect_host('185.154.14.162', 'crm_test', 'etl', 'etluser')
	return db

def get_db_connect_prod():
	db = db_sql.db_postgres()
	#db.connect_host('185.154.14.162', 'crm', 'etl', 'etluser')
	db.connect_host('185.154.14.162', 'crm', 'etl', 'etluser')
	return db


def main():
	conn = get_db_connect()
	print conn
	cur = conn.cursor()
	cur.execute("SELECT * FROM data.social_net;")
	rec = cur.fetchone()
	print rec
	return 0

if __name__ == '__main__':
	main()