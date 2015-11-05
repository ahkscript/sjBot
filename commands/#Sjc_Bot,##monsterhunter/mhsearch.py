#!/usr/bin/env python3


import json
import urllib


meta_data   = { "help": ["Returns a information about Monster Hunter","Usage: &botcmdmh <query>"], "aliases": ["mh", 'searchmh', 'monsterhunter'], "owner": 0 }
channel_specific = ['##monsterhunter']

def execute(parent, commands, user, host, channel, params):
    params = [urllib.parse.quote(x) for x in params]
    try:
        custom_search_key = parent.keys['kiranico']
        google_key = parent.keys['google']
        result = json.loads(parent.download_url('https://www.googleapis.com/customsearch/v1?key=' + google_key + '&cx=' + custom_search_key + '&q=' + '%20'.join(params)))
        items = result['items']
        if channel == '##monsterhunter':
            title = '\x02Here you go Doodle\x02'
        else:
            title = ' - '.join([x['title'] for x in items[0]['pagemap']['breadcrumb']])
        url = items[0]['link']
        return title + ' - ' + url
    except Exception as error:
        return ['Could not find that.']
    else:
        return ['Could not find that.']