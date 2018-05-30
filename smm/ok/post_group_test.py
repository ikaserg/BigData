# -*- coding: utf-8 -*-

import ok_api
import db_connect

def main():
    ok = ok_api.OdnoklassnikiRu()
    ok.getDefAuth()

    db = db_connect.get_db_connect()

    #resp, content = ok.getUploadUrl(gid = 52969628500104, count = 2)

    #resp, dis = ok.getPhotos(53985143554283, 53987273343211)

    imgs = ['E:\Grive\BigData\etl\smm\ok\image1.jpg', 'E:\Grive\BigData\etl\smm\ok\image2.jpg']

    #574248559595,

    db = db_connect.get_db_connect()
    i = 0
    img_b = []
    for x in db.do_query_all('select topic_image_id, theme_id, img from social.topic_images where topic_image_id > 1'):
        img_b.append(x[2])

    resp, dis = ok.postToGroup(52969628500104, 'Пробная тема', img_buf = img_b)

    print resp
    print dis

    #resp, dis = ok.getDiscussionsList(fields = 'object_type,title,creation_date')
    #resp, dis = ok.getDiscussionsList(fields = 'discussion.object_type')
    #print len(dis['discussions'])
    #print dis


    #resp, dis = ok.getUsersInfo(uids = [525167140079],
    #                            fields = 'first_name,last_name,gender,birthday,location,current_status,'\
    #                                     'current_status_id,current_status_date,url_profile,allows_anonym_access,'\
    #                                     'registered_date,premium')

    #print dis

main()