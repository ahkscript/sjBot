#!/usr/bin/env python3


def nick(con, sjBot, commands, trigger, host, channel, new_nickname):
    con.set_nickname(new_nickname)
    return None