#!/usr/bin/env python3


import urllib.parse
import json


aliases = ['#donationcoder']


def search(con, sjBot, commands, trigger, host, channel, *query):
    """Searches google for a donationcoder related query."""
    search = urllib.parse.quote(' '.join(query))
    raw_data = sjBot['url_download']('https://www.googleapis.com/customsearch'
               '/v1?key={}&cx=009062493091172133168:xwjfsl5agjc&q={}'.format(
                sjBot['settings']['google_key'], search))
    data = json.loads(raw_data)
    try:
        title = data['items'][0]['title']
        url = data['items'][0]['link']
        url = url.replace(';wap2', '')
        url = url.replace(';wap', '')
    except Exception:
        return 'Could not find info for that query.'
    return '\x02{}\x02 - {}'.format(urllib.parse.unquote(title), url)