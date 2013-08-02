#!/usr/bin/env python
# -*- utf-8 -*-
#=====================================================================================

import json, os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
    
from weibowrapper import sdk, conf
from weibowrapper.sdk import WeiboAccount

#=====================================================================================
# For Test
#=====================================================================================

myself = WeiboAccount(conf.uid_example, token=conf.token_example)

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

def get_all_archive(account, source='web'):
    if source == 'json':
        with open(conf.PATH_ARCHIVE_JSON, 'r') as f:
            feed_list = json.loads(f.read())
    else:
        query = {'count':50, 'page':1}
        first_round = True
        total = 1
        feed_list = []
        while (total > len(feed_list)):
            if first_round:
                result = account.call_api(conf.API_ARCHIVE, query)
                total = result['total_number']
                first_round = False
            else:
                result = account.call_api(conf.API_ARCHIVE, query)
                for entry in result['favorites']:
                    feed_list.append(entry['status'])
            query['page'] = query['page'] + 1
    return feed_list

def get_user_feed(account, uid):
    result = []
    base_path = conf.PATH_FEED_DB + '/' + uid + '/'
    if os.path.exists(base_path):
        for feed in os.listdir(base_path):
            with open(base_path+feed) as f:
                result.append(json.loads(f.read()))
    return result

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

def download_all_archive(account):
    query = {'count':50, 'page':1}
    first_round = True
    total = 1
    feed_list = []
    while (total > len(feed_list)):
        if first_round:
            result = account.call_api(conf.API_ARCHIVE, query)
            total = result['total_number']
            first_round = False
        else:
            result = account.call_api(conf.API_ARCHIVE, query)
        for entry in result['favorites']:
            feed_list.append(entry['status'])
        query['page'] = query['page'] + 1
    with open(conf.PATH_ARCHIVE_JSON, 'w') as f:
        f.write(json.dumps(feed_list))

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
# Search Functionality
#=====================================================================================

def db_pull_timeline(acocunt):
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

def index_db():
    schema = Schema( path     = TEXT(stored=True),
                     tweet_id = ID(stored=True),
                     content  = TEXT,
                     retweet  = TEXT )

    if not os.path.exists(conf.PATH_INDEX):
        os.mkdir(conf.PATH_INDEX)
    my_index = create_in(conf.PATH_INDEX, schema)
    my_writer = my_index.writer()

    for uid in os.listdir(conf.PATH_FEED_DB):
        for tweet in os.listdir(conf.PATH_FEED_DB+'/'+uid):
            rel_path = '/' + uid + '/' + tweet
            with open(conf.PATH_FEED_DB+rel_path, 'r') as f:
                doc = json.loads(f.read())
            if 'retweeted_status' in doc:
                my_writer.add_document( path     = rel_path, 
                                        tweet_id = str(doc['id']), 
                                        content  = doc['text'],
                                        retweet  = doc['retweeted_status']['text'])
            else:
                my_writer.add_document( path     = rel_path, 
                                        tweet_id = str(doc['id']), 
                                        content  = doc['text'],
                                        retweet  = '')                
    my_writer.commit()

def search_db(query_str):    
    my_index = open_dir(conf.PATH_INDEX)
    with my_index.searcher() as searcher:
        mparser = MultifieldParser(['content','retweet'], schema=my_index.schema)
        query = mparser.parse(query_str)
        results = searcher.search(query)
        feeds = []
        for path in [entry['path'] for entry in results]:
            with open(conf.PATH_FEED_DB+path,'r') as f:
                feeds.append(json.loads(f.read()))
        return feeds

def index_myfeed():
    schema = Schema( feed_id = ID(stored=True),
                     content = TEXT, 
                     retweet = TEXT)

    if not os.path.exists(conf.PATH_INDEX_MYFEED):
        os.mkdir(conf.PATH_INDEX_MYFEED)

    my_index = create_in(conf.PATH_INDEX_MYFEED, schema)
    my_writer = my_index.writer()
    with open(conf.PATH_MYFEED_JSON, 'r') as f:
        feeds = json.loads(f.read())
        for feed in feeds:
            if 'retweeted_status' in feed:
                my_writer.add_document( feed_id = str(feed['id']), 
                                        content = feed['text'],
                                        retweet = feed['retweeted_status']['text'])
            else:
                my_writer.add_document( feed_id = str(feed['id']), 
                                        content = feed['text'],
                                        retweet = '')
    my_writer.commit()

def search_myfeed(query_str):
    my_index = open_dir(conf.PATH_INDEX_MYFEED)
    with my_index.searcher() as searcher:
        mparser = MultifieldParser(['content','retweet'], schema=my_index.schema)
        query = mparser.parse(query_str)
        results = searcher.search(query)
        result_list = [entry['feed_id'] for entry in results]
        with open(conf.PATH_MYFEED_JSON,'r') as f:
            feeds = json.loads(f.read())
            return [feed for feed in feeds if str(feed['id']) in result_list]

def index_archive():
    schema = Schema( feed_id = ID(stored=True),
                     content = TEXT, 
                     retweet = TEXT)

    if not os.path.exists(conf.PATH_INDEX_ARCHIVE):
        os.mkdir(conf.PATH_INDEX_ARCHIVE)

    my_index = create_in(conf.PATH_INDEX_MYFEED, schema)
    my_writer = my_index.writer()
    with open(conf.PATH_ARCHIVE_JSON, 'r') as f:
        feeds = json.loads(f.read())
        for feed in feeds:
            if 'retweeted_status' in feed:
                my_writer.add_document( feed_id = str(feed['id']), 
                                        content = feed['text'],
                                        retweet = feed['retweeted_status']['text'])
            else:
                my_writer.add_document( feed_id = str(feed['id']), 
                                        content = feed['text'],
                                        retweet = '')
    my_writer.commit()

def search_my_archive(query_str):
    my_index = open_dir(conf.PATH_INDEX_ARCHIVE)
    with my_index.searcher() as searcher:
        mparser = MultifieldParser(['content','retweet'], schema=my_index.schema)
        query = mparser.parse(query_str)
        results = searcher.search(query)
        result_list = [entry['feed_id'] for entry in results]
        with open(conf.PATH_ARCHIVE_JSON,'r') as f:
            feeds = json.loads(f.read())
            return [feed for feed in feeds if str(feed['id']) in result_list]
        
def search_all(query_str):
    return search_db(query_str) + search_myfeed(query_str) + search_my_archive(query_str)
