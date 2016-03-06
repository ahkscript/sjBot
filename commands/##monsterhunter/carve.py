#!/usr/bin/env python3


import time
import random


carves = {'1-10': ['Plate', 'Pelt', 'Bone', 'Fang', 'Scale', 'Claw', 'Tail',
          'Wing', 'Talon'], '11-15': ['Ear', 'Fellwing', 'Shard', 'Ripper',
          'Cortex', 'Horn', 'Carapace', 'Marrow'], '16-18': ['Gem', 'Pallium',
          'Heart', '_You were tripped by a Konchu D:',
          '_You were rammed by a Rhenoplos D:']}


def carve(con, sjBot, commands, trigger, host, channel, person):
    """Carves a person. The person's name cannot have a space."""
    user = host.split('!')[0][1:]
    if 'carve_times' not in sjBot:
        sjBot['carve_times'] = {}

    print( sjBot['carve_times'] )

    if user in sjBot['carve_times']:
        user_info = sjBot['carve_times'][user]
        user_info['count'] += 1
        user_info['last'] = user_info['time']
        user_info['time'] = time.time()

        if (user_info['count'] >= 2 and user_info['time'] - 
                user_info['last'] < 60):
            return None
        elif (user_info['count'] >= 2 and user_info['time'] -
                user_info['last'] > 60):
            user_info['count'] = 0
    else:
        sjBot['carve_times'][user] = {'time': time.time(), 'count': 0,
                                      'last': 0}

    number = random.randint(0, 18)
    items = None
    for rarity in carves:
        low = int(rarity.split('-')[0])
        high = int(rarity.split('-')[1])
        if number >= low and number <= high:
            items = carves[rarity]
            break

    if items is None:
        return 'Nothing found! D:'
    item = random.choice(items)
    if item.startswith('_'):
        return item[1:]
    return "You got {}'s {}.".format(person, item)