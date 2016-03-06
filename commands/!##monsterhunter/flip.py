#!/usr/bin/env python3


import random


def flip(con, sjBot, commands, trigger, host, channel, *words):
    """Flips some letters."""
    faces = ['(╯°□°)╯', '(╯⌐■_■)╯', '(╯•_•)╯', '(╯ ͡° ͜ʖ ͡°)╯']
    if words == ():
        return '{} ︵ ┻━┻'.format(random.choice(faces))
    
    return None