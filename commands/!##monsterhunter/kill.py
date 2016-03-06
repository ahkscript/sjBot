#!/usr/bin/env python3


import random


def kill(con, sjBot, commands, trigger, host, channel, person, *weapon):
    """Kills a person with a random or specified weapon."""
    weapons = ['a small lion.', 'a dictionary', 'an angry mountain.',
               'the power of 3.', 'a honey badger.', 'a Hyper beam.',
               'a short drop and a sudden stop.',
               'a spoon, because knives are too easy.', 'a bowtie.',
               'tlm.', 'a rraaaiiinnboww trout.', 'bordem.',
               'the power of 1000 suns.']
    if len(weapon) == 0:
        weapon = random.choice(weapons)
    else:
        weapon = ' '.join(weapon)
    return '\x01ACTION kills {} with {}\x01'.format(person, weapon)