import psycopg2
import numpy as np
import db_connect
#import libpq-dev

def read_file(file_name):
    f = open(file_name, 'rb')
    data = psycopg2.Binary(f.read())
    f.close()
    return data

db = db_connect.get_db_connect_prod()
#i = 0
#for x in db.do_query_all('select topic_image_id, theme_id, img from social.topic_images where topic_image_id > 1'):
#    f = open('d:\\'+str(i)+'.jpg', 'wb')
#    f.write(str(x[2]))
#    f.close()
#    i += 1



db.exec_query('delete from social.topic_images')

db.exec_query_params("insert into social.topic_images values(1, 2, %(img)s)",
                     {'img' :  read_file('e:\Grive\BigData\etl\images\land1.jpg')})
db.exec_query_params("insert into social.topic_images values(2, 2, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\land2.png')})

db.exec_query_params("insert into social.topic_images values(3, 3, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\\family1.jpg')})
db.exec_query_params("insert into social.topic_images values(4, 3, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\\family2.jpg')})

db.exec_query_params("insert into social.topic_images values(5, 1, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\grinina1.jpg')})
db.exec_query_params("insert into social.topic_images values(6, 1, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\morozkina1.jpg')})

db.exec_query_params("insert into social.topic_images values(7, 4, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\criminal1.jpg')})
db.exec_query_params("insert into social.topic_images values(8, 4, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\criminal2.jpg')})

db.exec_query_params("insert into social.topic_images values(9, 5, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\customer1.jpg')})
db.exec_query_params("insert into social.topic_images values(10, 5, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\customer2.jpg')})

db.exec_query_params("insert into social.topic_images values(11, 6, %(img)s)",
                     {'img': read_file('e:\Grive\BigData\etl\images\karpukhin1.jpg')})

db.exec_query('commit')
