#!/usr/bin/env python
# -*- utf-8 -*-
#=====================================================================================

import json, os
from weibowrapper import sdk, conf

#=====================================================================================
# Online API wrapper
#=====================================================================================

def get_all_follower (account, source='web', target='return'):
    if source == 'json':
        with open(conf.PATH_FOLLOWER_JSON, 'r') as f:
            follower_list = json.loads(f.read())
    else:
        query = {'count': 200}
        result = account.call_api(conf.API_FOLLOWER, query)
        follower_list = result['users']
        while (result['next_cursor'] != 0):
            query['cursor'] = result['next_cursor']
            result = account.call_api(conf.API_FOLLOWER, query)
            follower_list += result['users']
    if target == 'return':
        return follower_list
    else:
        with open(conf.PATH_FOLLOWER_JSON, 'a') as f:
            f.write(json.dumps(follower_list))

def get_all_following (account, source='web', target='return'):
    if source == 'json':
        with open(conf.PATH_FOLLOWING_JSON, 'r') as f:
            following_list = json.loads(f.read())
    else:
        query = {'count': 200}
        result = account.call_api(conf.API_FOLLOWING, query)
        following_list = result['users']
        while (result['next_cursor'] != 0):
            query['cursor'] = result['next_cursor']
            result = account.call_api(conf.API_FOLLOWING, query)
            following_list += result['users']
    if target == 'return':
        return following_list
    else:
        with open(conf.PATH_FOLLOWING_JSON, 'a') as f:
            f.write(json.dumps(following_list))

def get_all_myfeed(account, source='web', target='return'):
    if source == 'json':
        with open(conf.PATH_MYFEED_JSON, 'r') as f:
            myfeed_list = json.loads(f.read())
    else:
        query = {'count': 100}
        result = account.call_api(conf.API_MYFEED, query)
        myfeed_list = result['statuses']
    if target == 'return':
        return myfeed_list
    else:
        with open(conf.PATH_MYFEED_JSON, 'a') as f:
            f.write(json.dumps(myfeed_list))

#=====================================================================================
# Local Database
#=====================================================================================

def db_pull_timeline(acocunt):
    '''
    Pull your entire timeline (all feeds you received) to local, in DATA_PATH/feeddb/uid/id
    '''
    in_progress = True
    first_round = True
    while (in_progress):
        if first_round:
            result = acocunt.call_api(conf.API_TIMELINE, {'count':100})
            first_round = False
        else:
            result = acocunt.call_api(conf.API_TIMELINE, {'count': 100, 'max_id': result['next_cursor']})
        for tweet in result['statuses']:
            path = conf.PATH_FEED_DB + '/' + str(tweet['user']['id'])
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path+'/'+str(tweet['id']), 'w') as f:
                f.write(json.dumps(tweet))
        if result['next_cursor'] == 0:
            in_progress = False

