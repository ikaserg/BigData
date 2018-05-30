# -*- coding: utf-8 -*-

import httplib2
import urllib

class SocialNet(object):
    def __init__(self):
        self.token = ''
        self.secret_key = ''
        self.user_id = 0
        self.base_url = ''
        self.def_param = ''
        self.application_key = 0

    def getDefAuth(self):
        return 0

    def subParams(self, url, params):
        res_url = url
        if not res_url.endswith('&') and not res_url.endswith('?'):
            res_url += '&'
        res_url += urllib.urlencode(params)
        return res_url


    def callMethod(self, name, params):
        url = self.subParams(self.base_url, {'method':name})
        url = self.subParams(url, self.def_params)
        url = self.subParams(url, params)
        resp, content = httplib2.Http().request(url)
        return resp, content

    def callPostMethod(self, name, params):
        url = self.subParams(self.base_url, {'method': name})
        url = self.subParams(url, self.def_params)
        url = self.subParams(url, params)
        resp, content = httplib2.Http().request(url)
        return resp, content



