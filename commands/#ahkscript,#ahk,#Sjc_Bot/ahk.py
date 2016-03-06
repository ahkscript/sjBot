#!/usr/bin/env python3


import re
import urllib.parse
import json
import difflib


owner = False
aliases = ['ahksearch', 'search', 'a']


def ahk(con, sjBot, commands, trigger, host, channel, *query):
    """Searches the AHK docs for something. If its not found it will
    then search the forum."""

    with open('commands/docs.json') as dfile:
        links = json.loads(dfile.read())

    matches = difflib.get_close_matches(' '.join(query).lower(), links, cutoff=0.5)
    if len(matches) > 0:
        return '\x02{}\x02 - http://ahkscript.org/docs/{}'.format(matches[0],
                links[matches[0]])

    search = urllib.parse.quote(' '.join(query))

    data = json.loads(sjBot['url_download']('https://www.googleapis.com/'
        'customsearch/v1?key={}&cx=009062493091172133168:_o2f4moc9ce&q='
        '{}'.format(sjBot['settings']['google_key'], search)))

    print( data['searchInformation']['totalResults'] == '0' )
    if data['searchInformation']['totalResults'] == '0':
        return 'No information found.'

    if len(data['items']) > 0:
        item = data['items'][0]
        return '\x02{}\x02 - {}'.format(data['items'][0]['title'],
                                 data['items'][0]['formattedUrl'])
    return None