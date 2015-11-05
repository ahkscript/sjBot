#!/usr/bin/env python3


import time


meta_data   = { "help": ["Creates and manages a room for specific hunts.","&botcmdhunt create <room name> <room id> [description]", "&botcmdhunt list [search keywords]", "&botcmdhunt id <room name> <new id> (If you are in a room you don't need <room name>)", "&botcmdhunt remove <room name> (You don't need room name if you are in a room)"], "aliases": ["hunt", "huntroom", "mhroom"], "owner": 0 }
channel_specific = ['##monsterhunter']


def create(sjBot, user, name, id, *description):
    name = name.lower()
    if name in sjBot.hunting_rooms:
        return ['That is already a room.']
    sjBot.hunting_rooms[name] = {'description': ['No description'], 'people': [], 'name': name, 'id': id, 'creator': user, 'time': time.time()}
    if len(description) > 0:
        sjBot.hunting_rooms[name]['description'] = description
    sjBot.join('##monsterhunter-' + name)
    return ['I have created the room: ##monsterhunter-' + name]


def list(sjBot, user, *keywords):
    channels = [sjBot.hunting_rooms[x] for x in sjBot.hunting_rooms]
    sjBot.privmsg(user, 'Here is a list of rooms: ')
    for index, room in enumerate(channels):
        players = 'people: ' + str(len(room['people']))
        description = ' '.join(room['description'])
        name = room['name']
        id = room['id']
        if keywords != ():
            print( any(x in name for x in keywords) )
            if any(x.lower() in name.lower() for x in keywords) is False and any(x.lower() in description.lower() for x in keywords) is False:
                continue
        sjBot.privmsg(user, '{} - id: {}, {} - {}'.format('##monsterhunter-' + name, id, players, description))
        if index > 10:
            time.sleep(1)
    return None


def id(sjBot, user, name, new_id):
    name = name.lower()
    if name not in sjBot.hunting_rooms:
        return ['Could not find that room.']
    if user != sjBot.hunting_rooms[name]['creator']:
        return ['You do not have permission to do that']
    sjBot.hunting_rooms[name]['id'] = new_id
    return ['Changed ID']


def password(sjBot, user, name, new_pass):
    name = name.lower()
    if name not in sjBot.hunting_rooms:
        return ['Could not find that room.']
    if user != sjBot.hunting_rooms[name]['creator']:
        return ['You do not have permission to do that']
    sjBot.hunting_rooms[name]['pass'] = new_pass
    return None


def remove(sjBot, user, name):
    name = name.lower()
    if name not in sjBot.hunting_rooms:
        return ['Could not find that room.']
    if user != sjBot.hunting_rooms[name]['creator']:
        return ['You do not have permission to do that']
    del sjBot.hunting_rooms[name]
    sjBot.send('PART ##monsterhunter-' + name)
    return ['Removed hunting room: ' + name]


def execute(sjBot, commands, user, host, channel, params):
    if channel.startswith('##monsterhunter-'):
        params[0] = channel.replace('##monsterhunter-', '')
    if hasattr(sjBot, 'hunting_rooms') is False:
        sjBot.hunting_rooms = {}
    commands = {'create': create, 'list': list, 'id': id, 'remove': remove}
    if params[0] in commands:
        return commands[params[0]](sjBot, user, *params[1:])
    return ['That is not a room command.']