from okwalker import OkWalker
from db_connect import get_db_connect
import ok_api
import ok_friend_stat

def main():
    db = get_db_connect()
    ok = ok_api.OdnoklassnikiRu()
    ok.getDefAuth()

    ok_srv = ok_friend_stat.OkServices(ok, db)

    ok_srv.collectMsgUserInfo()

main()