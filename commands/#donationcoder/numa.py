#!/usr/bin/env python3


import random


def numa(con, sjBot, commands, trigger, host, channel):
    """Does the numa numa dance!"""
    movements = ['.o.', '\\o/', '\o\\', '/o/']
    output = 'Maia-hee, maia-huu, maia-hoo, maia-haha. '
    for i in range(random.randint(4, 8)):
        output += '\x03{}{}\x03 '.format(random.randint(1, 9),
                  random.choice(movements))
    return output