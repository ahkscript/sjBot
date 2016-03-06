#!/usr/bin/env python3


import json
import urllib.parse


aliases = ['w']


def wiki(con, sjBot, commands, trigger, host, channel, *query):
    search = urllib.parse.quote(' '.join(query))
    download = sjBot['url_download']
    api_key = sjBot['settings']['google_key']
    query_result = download('https://www.googleapis.com/customsearch/v1'
                            '?key={}&cx=009062493091172133168:4ckmchbpuzy&'
                            'q=site:en.wikipedia.org%20{}'.format(api_key,
                            search))
    query_data = json.loads(query_result)
    try:
        search_result = query_data['items'][0]
        url = search_result['formattedUrl']
    except Exception:
        return 'No results found.'
    return '\x02{}\x02 - {}'.format(' '.join(query), url)