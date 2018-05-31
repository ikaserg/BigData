# -*- coding: utf-8 -*-
import sm_api
import hashlib
import json
import requests
import io

UPLOAD_URL = ''

class OdnoklassnikiRu(sm_api.SocialNet):
    def __init__(self):
        self.def_params = {}
        self.social_id = 3

    def __setattr__(self, name, value):
        if hasattr(self, 'def_params'):
            if name == 'token':
                self.def_params['access_token'] = value
            if name == 'application_key':
                self.def_params['application_key'] = value
        super(OdnoklassnikiRu, self).__setattr__(name, value)

    def getDefAuth(self):
        self.token = 'tkn1UI4z0QIiVWlVELixiRAqYne564oqLcs5OrwUKq0RgvHEnpxUhoChw4fQIv4EF3sc9'
        self.session_secret_key = '3348a373acb5ecaead2b861b41fee11f'
        self.user_id = 574248559595
        self.base_url = 'http://api.ok.ru/fb.do?'
        self.application_id = 1247354624
        self.application_key = 'CBAQBKFLEBABABABA'
        self.application_secret_key = '23A1E586975677B64EEAF02F'
        self.def_params = {'application_key': self.application_key, 'format':'JSON', 'access_token': self.token}

    def getAndrewAuth(self):
        self.token = 'tkn1kIUFnd83fuQhCm9PJaCIeQvvpSrl6WBbrKp9ZuC3GGYwsOOfqjgapQvGawq6dNjIo0'
        self.session_secret_key = '67a738e1d0f18ad3e88990f8b51f7902'
        self.user_id = 575918147556
        self.base_url = 'http://api.ok.ru/fb.do?'
        self.application_id = 1247354624
        self.application_key = 'CBAQBKFLEBABABABA'
        self.application_secret_key = '23A1E586975677B64EEAF02F'
        self.def_params = {'application_key': self.application_key, 'format': 'JSON', 'access_token': self.token}

    def callMethod(self, name, params):
        sig_param = params.copy()
        sig_param['application_key'] = self.def_params['application_key']
        sig_param['format'] = self.def_params['format']
        sig_param['method'] = name
        p = ''.join(['%s=%s' % (key, value) for key, value in sorted(sig_param.items())]) + self.session_secret_key
        params['sig'] = hashlib.md5(p).hexdigest()
        resp, content = sm_api.SocialNet.callMethod(self, name, params)
        return resp, json.loads(content)

    def getOnlineFriends(self, uid):
        return self.callMethod('friends.getOnline', {'uid':uid})

    def getOnlineFriends(self):
        resp, content = self.callMethod('friends.getOnline', {})
        return resp, content

    def getFriends(self):
        resp, content = self.callMethod('friends.get', {})
        return resp, content

    def getDiscussionsList(self, types = None, category='MY', fields = None):
        params = {}
        if types is not None:
            params = {'types': types}
        if category is not None:
            params['category'] = category
        if fields is not None:
            params['fields'] = fields

        resp, content = self.callMethod('discussions.getList', params)
        return resp, content

    def getUsersInfo(self, uids, fields):
        params = {}
        if uids is not None:
            params['uids'] = ','.join([str(x) for x in uids])

        if uids is not None:
            params['fields'] = fields

        resp, content = self.callMethod('users.getInfo', params)
        return resp, content

    #def load_photo(self):
    #838519070955
    def getPhotos(self, gid, aid):
        resp, content = self.callMethod('photos.getPhotos',{'gid': gid, 'aid': aid, 'count': 10})
        return resp, content

    def getUploadUrl(self, gid, count):
        resp, content = self.callMethod('photosV2.getUploadUrl',{'gid': gid, 'count': count})
        return resp, content

    def uploadPhotos(self, gid, images):
        resp, content = self.getUploadUrl(gid, len(images))

        url = content['upload_url']
        photo_ids = content['photo_ids']

    def postToGroup(self, gid, txt = None, img_buf = None, images = None, post_at = None):
        # получение url для загрузки
        l = 0
        if images is not None:
            l += len(images)
        if img_buf is not None:
            l += len(img_buf)

        resp, content = self.getUploadUrl(gid, l)

        # загрузка иображений на сервер

        url = content['upload_url']
        photo_ids = content['photo_ids']

        files = {}
        id_list = []
        i = 0

        if images is not None:
            for img in images:
                files['file' + str(i)] = open(img, 'rb')
                i += 1

        if img_buf is not None:
            for img in img_buf:
                files['file' + str(i)] = io.BytesIO(img)
                i += 1

        r = requests.post(url, files=files)

        for f in range(i):
            id_list.append({'id': json.loads(r.content)['photos'][photo_ids[i - 1 - f]]['token']})

        media = []
        media.append({'type' : 'text', 'text' : txt})
        #for img in images:

        att = {"media": [
                    {'type' : 'text',
                     'text' : txt
                     },
                    {
                        "type": "photo",
                        "list": id_list
                    },
               ]}

        if post_at is not None:
            att['publishAtMs'] = str(post_at)
        return self.callMethod('mediatopic.post',
                               {'type': 'GROUP_THEME',
                                'gid': gid,
                                'attachment': json.dumps(att)})

        return 0

    def collectMsgUserInfo(self, wnd = 100):
        sql = 'select m.from_user_id '\
              '  from social.messages m ' \
              ' where m.from_user_id not in (select u.user_id' \
              '                                from social.users u) ' \
              'union ' \
              'select m.to_user_id '\
              '  from social.messages m ' \
              ' where m.to_user_id not in (select u.user_id' \
              '                              from social.users u)'

        uids = [x[0] for x in self.db.do_query_all(sql)]

        uid_cnt = len(uids)
        x = 0
        while x < uid_cnt:
            l = min(wnd, uid_cnt - x)
            r, ui = self.api.getUsersInfo(uids[x: x + l], self.fields)
            self.updateUserInfo(ui)
            x += l

        return 0
