#!/usr/bin/env python
# -*- utf-8 -*-
#=====================================================================================

import json, os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
    
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
# Local Image
#=====================================================================================

def download_all_follower (account):
    query = {'count': 200}
    result = account.call_api(conf.API_FOLLOWER, query)
    follower_list = result['users']
    while (result['next_cursor'] != 0):
        query['cursor'] = result['next_cursor']
        result = account.call_api(conf.API_FOLLOWER, query)
        follower_list += result['users']
    for profile in follower_list:
        os.system('wget -O ' + conf.PATH_AVATAR + '/' + profile['idstr'] + '.jpg ' + profile['avatar_large'])
    with open(conf.PATH_FOLLOWER_JSON, 'w') as f:
        f.write(json.dumps(follower_list))
            
def download_all_following (account):
    query = {'count': 200}
    result = account.call_api(conf.API_FOLLOWING, query)
    following_list = result['users']
    while (result['next_cursor'] != 0):
        query['cursor'] = result['next_cursor']
        result = account.call_api(conf.API_FOLLOWING, query)
        following_list += result['users']
    for profile in following_list:
        os.system('wget -O ' + conf.PATH_AVATAR + '/' + profile['idstr'] + '.jpg ' + profile['avatar_large'])
    with open(conf.PATH_FOLLOWING_JSON, 'w') as f:
        f.write(json.dumps(following_list))

def download_all_myfeed(account):
    result = account.call_api(conf.API_MYFEED, {'count': 100})
    myfeed_list = result['statuses']
    with open(conf.PATH_MYFEED_JSON, 'w') as f:
        f.write(json.dumps(myfeed_list))

def download_all_timeline(acocunt):
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

def db_index():

    schema = Schema( path     = TEXT(stored=True),
                     tweet_id = ID(stored=True),
                     content  = TEXT )

    if not os.path.exists(conf.PATH_INDEX):
        os.mkdir(conf.PATH_INDEX)

    my_index = create_in(conf.PATH_INDEX, schema)
    my_writer = my_index.writer()

    for uid in os.listdir(conf.PATH_FEED_DB):
        for tweet in os.listdir(conf.PATH_FEED_DB+'/'+uid):
            rel_path = '/' + uid + '/' + tweet
            with open(conf.PATH_FEED_DB+rel_path, 'r') as f:
                doc = json.loads(f.read())
            my_writer.add_document( path     = rel_path, 
                                    tweet_id = str(doc['id']), 
                                    content  = doc['text'])
    my_writer.commit()

def db_search(query_str):    
    my_index = open_dir(conf.PATH_INDEX)
    with my_index.searcher() as searcher:
        query = QueryParser('content', my_index.schema).parse(query_str)
        results = searcher.search(query)
        print(results)
        for entry in results:
            print(entry)

