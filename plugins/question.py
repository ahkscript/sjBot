#!/usr/bin/env python3


activate = ['what is the', 'find the']


def r_PRIVMSG(con, sjBot, user, channel, *message):
    for phrase in activate:
        if ' '.join(message).startswith(':{}: {}'.format(con.nickname, phrase)):
            pass
    return None