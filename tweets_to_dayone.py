#!/usr/bin/env python

import os, sys
import json
from dateutil import parser
from datetime import datetime
from pprint import pprint
from dayone import add_dayone_entry
from tempfile import NamedTemporaryFile
import requests

def main():
    # process each js file in the list of arguments
    for f in sys.argv[1:]:
        process_tweet_archive(f)

def process_tweet_archive(infile):
    tweets = {}
    with open(infile) as f:
        f.readline()
        tweets = json.load(f)
    for t in tweets:
        try:
            log_tweet(t)
        except Exception as e:
            print e
            print t
            print

def log_tweet(t):
    d = parser.parse(t['created_at'])
    t = process_links(t)
    text = '{0} (@{1})\n'.format(t['user']['name'], t['user']['screen_name'])
    text += '{0}\n'.format(t['text'].encode('utf-8'))
    text += '[View on Twitter](https://twitter.com/edgauthier/statuses/{0})'.format(t['id'])
    text = text.decode('utf-8')
    photos = get_photos_from_tweet(t)
    if len(photos):
        for p in photos:
            add_dayone_entry(creation_date=d, entry_text=text, tags=['Social', 'Twitter'], photo=p)
    else:
        add_dayone_entry(creation_date=d, entry_text=text, tags=['Social', 'Twitter'], photo=None)
    if len(photos):
        for p in photos:
            os.remove(p)

def process_links(t):
    text = t['text']
    if 'entities' in t and 'urls' in t['entities']:
        urls = t['entities']['urls']
        url_map = {}
        for url in urls:
            old = url['url']
            new = u'[{0}]({1})'.format(url['display_url'], url['expanded_url'])
            text = text.replace(old, new)
    t['text'] = text
    return t

def get_photos_from_tweet(t):
    photos = []
    try:
        if 'entities' in t and 'media' in t['entities']:
            media = t['entities']['media']
            for m in media:
                media_url = m['media_url'] + ':large'
                p = download_file(media_url)
                photos.append(p)
    except Exception as e:
        print 'Error getting photos: {0}'.format(e)
    return photos

def download_file(url):
    local_filename = get_temp_path()
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

def get_temp_path():
    f = NamedTemporaryFile(delete=False)
    path = f.name
    f.close()
    return path

if __name__ == '__main__':
    main()
