#!/usr/bin/env python
# -*- utf-8 -*-
#----------------------------------------------------------------------------------
# This is the SDK of Sina Weibo
#----------------------------------------------------------------------------------

import sqlite3 as sqlite
import sys, os, urllib, json

try:
    import requests
except:
    print("do not have requests installed, can't access API through web")

from weibowrapper import conf



#----------------------------------------------------------------------------------
# User Interface
#----------------------------------------------------------------------------------

class WeiboAccount(object):

    def __init__(self, uid, token=None):
        self.uid = uid
        self.access_token = token
        self.user_info = { 'access_token': self.access_token }

    def call_api(self, api, query):
        query['access_token'] = self.access_token
        resp = requests.get(api, params=query)
        return resp.json()

    def get_oauth_uri(self):
        query = { 'client_id': conf.client_key, 
                  'response_type': 'code', 
                  'redirect_uri': conf.redirect_uri}
        return OAUTH_AUTHORIZE + '?' + urllib.urlencode(query)

    def get_oauth_token(self, code):
        query = {
            'client_id': conf.client_key,
            'client_secret': conf.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': conf.redirect_uri,
            'code': code}
        resp = requests.post(OAUTH_GET_TOKEN, params=query)
        self.access_token = resp.json()['access_token']


#----------------------------------------------------------------------------------
# OAuth Methods
#----------------------------------------------------------------------------------
# Authorization Steps
# 1. login_request -> send login.html to user browser
# 2. get_sina_code -> receive CODE from sina
# 3. request_sina_token -> use code and app info request for token
#----------------------------------------------------------------------------------









#----------------------------------------------------------------------------------
# Execute
#----------------------------------------------------------------------------------

if __name__ == '__main__':
    print('use python -i to run this module interactively')


#----------------------------------------------------------------------------------
# Test
#----------------------------------------------------------------------------------
