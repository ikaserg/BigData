from okwalker import OkWalker
from db_connect import get_db_connect
import ok_api
import ok_services

def main():
    db = get_db_connect()
    ok = ok_api.OdnoklassnikiRu()
    ok.getDefAuth()

    ok_srv = ok_services.OkServices(ok, db)

    #
    ok_srv.appendMsgUsers()

main()