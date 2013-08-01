#!/usr/bin/env python

import os, urllib

#----------------------------------------------------------------------------------
# Weibo Authentication Information
#----------------------------------------------------------------------------------

client_key    = '2830674174'
client_secret = '3d2e9e2a46a2349473041cf276751f47'
api_key       = ''
access_scope  = ''
redirect_uri  = 'http://216.24.205.41/sina-token'

token_example = '2.003WDnhCEfNZFDc811f9ffa9TP9iwB'
uid_example   = '2479339722'

#----------------------------------------------------------------------------------
# Persistent Related Constants
#----------------------------------------------------------------------------------

PATH_DATA   = os.environ['HOME'] + '/Persistent/Weibo'

PATH_FEED_DB = PATH_DATA + '/feeddb'
PATH_INDEX   = PATH_DATA + '/index'
PATH_IMAGE   = PATH_DATA + '/image'
PATH_AVATAR  = PATH_DATA + '/avatar'

PATH_FOLLOWING_JSON = PATH_DATA + '/following.json'
PATH_FOLLOWER_JSON  = PATH_DATA + '/follower.json'
PATH_MYFEED_JSON    = PATH_DATA + '/myfeed.json'

#----------------------------------------------------------------------------------
# API URI Constants
#----------------------------------------------------------------------------------

API_BASE = 'https://api.weibo.com/2'

API_FOLLOWER  = '/friendships/followers.json'
API_FOLLOWING = '/friendships/friends.json'
API_MYFEED    = '/statuses/user_timeline.json'
API_TIMELINE  = '/statuses/home_timeline.json'

OAUTH_AUTHORIZE = 'https://api.weibo.com/oauth2/authorize'
OAUTH_GET_TOKEN = 'https://api.weibo.com/oauth2/access_token'

#OAUTH_URL = OAUTH_AUTHORIZE + '?' + urllib.urlencode( {'client_id': client_key, 
#                                                       'response_type': 'code', 
#                                                       'redirect_uri': redirect_uri} )
