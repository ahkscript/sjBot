#!/usr/bin/env python3


import urllib.parse
import json


aliases = ['g']


def google(con, sjBot, commands, trigger, host, channel, *query):
    """Searches google for a query"""
    search = urllib.parse.quote(' '.join(query))
    download = sjBot['url_download']
    result = download('http://ajax.googleapis.com/ajax/services/search'
                          '/web?v=1.0&q={}'.format(search))
    search_data = json.loads(result)
    try:
        search_result = search_data['responseData']['results'][0]
        title = search_result['titleNoFormatting']
        url = search_result['url']
    except Exception:
        return 'No results found.'
    return '\x02{}\x02 - {}'.format(title, url)