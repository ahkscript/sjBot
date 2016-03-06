#!/usr/bin/env python3


import urllib.parse
import json


aliases = ['4u', 'mh', 'm4', 'mh4']


def mh4u(con, sjBot, commands, trigger, host, channel, *query):
    """Searches kiranico for a mh4u related query"""
    search = urllib.parse.quote(' '.join(query))
    google_key = sjBot['settings']['google_key']
    search_key = sjBot['settings']['kiranico']['mh4u']
    download = sjBot['url_download']
    result = download('https://www.googleapis.com/customsearch/v1?key={}'
                      '&cx={}&q={}'.format(google_key, search_key, search))
    search_result = json.loads(result)
    try:
        item = search_result['items'][0]
        url = item['link']
    except Exception:
        return 'Could not find that.'
    return '\x02Here you go Doodle\x02 - {}'.format(url)