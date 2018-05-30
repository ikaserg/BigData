import psycopg2


# Соединение с базой данных
def get_db_connect():
	return psycopg2.connect("dbname='smtrade' user='smtrade' password='smtrade'")

#  Загрузка файла
def load_file(file_name, file_cont, db_conn):
	

def main():
	conn = get_db_connect()
	print conn
	cur = conn.cursor()
	cur.execute("SELECT * FROM log_load;")
	rec = cur.fetchone()
	print rec
	return 0

if __name__ == '__main__':
	main()
	
