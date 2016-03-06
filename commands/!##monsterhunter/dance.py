#!/usr/bin/env python3


import random


owner = False
aliases = ['moveyourbooty']


def dance(con, sjBot, commands, trigger, host, channel, person=None):
    """Shows some dance moves. Optionally dances with someone."""
    movements = ['\\o\\', '/o/', '\\o/', '\\o_', '_o/']
    if person is not None:
        output = 'Dance with me {}! '.format(person)
    else:
        output = 'Dance! '
    for i in range(random.randint(4, 8)):
        output += '\x03{}{}\x03 '.format(random.randint(1, 9),
                  random.choice(movements))
    return output