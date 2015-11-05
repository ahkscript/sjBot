#!/usr/bin/env python3


import random


meta_data   = { "help": ["Carves out an item from a person.","Usage: &botcmdcarve <person>"], "aliases": ["cv", "carve"], "owner": 0}
carves = {'1-10': ['Plate', 'Pelt', 'Bone', 'Fang', 'Scale', 'Claw', 'Tail', 'Wing', 'Talon'], '11-15': ['Ear', 'Fellwing', 'Shard', 'Ripper', 'Cortex', 'Horn', 'Carapace', 'Marrow'], '16-18': ['Gem', 'Pallium', 'Heart']}


def execute(sjBot, commands, user, host, channel, params):
    if len(params) < 1:
        return "I don't know who to carve!"
    person = ' '.join(params[0:])
    number = random.choice(range(18))
    items = None
    for rareity in carves:
        low = int(rareity.split('-')[0])
        high = int(rareity.split('-')[1])
        print( low )
        print( high )
        if number >= low and number <= high:
            items = carves[rareity]
    if items == None:
        return 'Nothing found!'
    item = random.choice(items)
    return "You got {}'s {}.".format(person, item)