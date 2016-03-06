#!/usr/bin/env python3


import re


words = ['fuck', 'cunt', 'dick', 'slut', 'nigger', 'fuk']
channels = ['#ahkscript', '#ahk']


def r_PRIVMSG(con, sjBot, user, channel, *message):
    if channel not in channels:
        return None
    for word in words:
        match = ''.join(['{}+?'.format(x) for x in word])
        swear_match = re.search(match, ' '.join(message), re.IGNORECASE)
        if swear_match is not None:
            con.privmsg(channel, 'This is a PG channel, no profanity '
                        '{}.'.format(user.split('!')[0][1:]))
    return None