#!/usr/bin/env python3


import json
import urllib.parse


def define(con, sjBot, commands, trigger, host, channel, *words):
    """Finds the meaning of a word."""
    search = urllib.parse.quote(' '.join(words))
    raw_data = sjBot['url_download']('http://api.wordnik.com/v4/word.json/{}/'
               'definitions?limit=200&includeRelated=true&useCanonical=false'
               '&includeTags=false&api_key={}'.format(search,
                sjBot['settings']['wordnik_key']))
    data = json.loads(raw_data)
    try:
        word = data[0]['word']
        info = data[0]['text']
    except (IndexError, ValueError):
        return 'Could not find info for that word.'
    return '\x02{}\x02 - {}'.format(word, info)