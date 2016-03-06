#!/usr/bin/env python3


def join(con, sjBot, commands, trigger, host, channel, channels):
    """Joins a comma seperated list of channels."""
    con.send('JOIN {}'.format(channels))
    return None