#!/usr/bin/env python3


import json
import re


def info(con, sjBot, commands, trigger, host, channel, *command):
    """Gets info about AutoHotkey commands."""
    command = ' '.join(command).strip()
    with open('commands/docs.json', 'r') as dfile:
        docs = json.loads(dfile.read())
    if command not in docs:
        return 'Could not find that command.'
    download = sjBot['url_download']
    url = 'http://autohotkey.com/docs/{}'.format(docs[command])
    html = download(url)
    info_match = re.search('<p>(.*?)</p>.*?<pre .*?>(.*?)</pre',
                           html, re.DOTALL)
    if info_match is None:
        return 'Could not find info about that command.'
    return [info_match.group(1), info_match.group(2)]