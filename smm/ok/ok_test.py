import ok_api
import db_connect
import ok_services

def main():
    ok = ok_api.OdnoklassnikiRu()
    ok.getDefAuth()

    db = db_connect.get_db_connect()

    ok_srv = ok_services.OkServices(ok, db)

    ok_srv.addNewFriends()
    ok_srv.collectNewInfo()



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