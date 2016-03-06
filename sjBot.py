#!/usr/bin/env python3


import datetime
import time
import imp
import json
import os
import sys
import urllib.request
import inspect
import simple_ui
import threads
import base


commands = {}
plugins = {}
realpath = os.path.dirname(os.path.realpath(__file__))
settings = {}
connections = {}


def ui_message(ui, message):
    network = ui.network
    channel = ui.channel

    if message.startswith('/refresh'):
        ui.refresh_all()
        return None

    if message.startswith('/join'):
        connections[ui.network].join(message.split(' ')[1])
        return None

    if message.startswith('/channel'):
        ui.channel = message.split(' ')[1]
        return None

    if message.startswith('/server'):
        ui.network = message.split(' ')[1]
        return None

    # I would rather use the real value None but for some reason
    # it was not working here. So it's a string 'None'.

    if network == 'None':
        return

    if channel != 'None':
        message = 'PRIVMSG {} :{}'.format(channel, message)

    connection = connections[network]
    connection.send(message)
    return None


def r_PING(con, *params):
    con.send('PONG {}'.format(params[0]))
    return None


def r_422(con, *params):
    channels = settings['connections'][con.network]['channels']
    for channel in channels:
        con.join(channel)
    return None


def r_433(con, *junk):
    con.set_nickname(con.nickname + '_')
    return None


def r_376(con, *junk):
    info = settings['connections'][con.network]
    con.privmsg('NickServ', 'Identify {} {}'.format(info['nickname'],
                info['nickserv_password']))
    return None


def r_396(con, *junk):
    channels = settings['connections'][con.network]['channels']
    for channel in channels:
        con.join(channel)
    return None


def r_ERROR(con, *information):
    lethal = ['Closing Link', 'Ping Timeout']
    if any(err_type in ' '.join(information) for err_type in lethal):
        connected = con.reconnect()
        if not connected:
            con.close_connection()
    return None


def r_ALL(con, *message):
    for plugin in plugins:
        source = plugins[plugin]
        params = list(message)
        try:
            if hasattr(source, 'r_' + message[0]):
                getattr(source, 'r_' + message[0])(con, globals(),
                        *message[1:])
            if hasattr(source, 'r_' + message[1]):
                getattr(source, 'r_' + message[1])(con, globals(), 
                        *[params[0]] + params[2:])
        except Exception as e:
            print('Error {} in plugin {}'.format(e, plugin))
    return None


@threads.asthread()
def r_PRIVMSG(con, user, channel, *message):
    triggers = settings['connections'][con.network]['trigger']
    if '__botname__' in triggers:
        triggers[con.nickname] = triggers['__botname__']
        del triggers['__botname__']
    if channel not in triggers:
        trigger = triggers['default']
    else:
        trigger = triggers[channel]

    if len(' '.join(message)) == len(trigger) or ' '.join(message)[len(trigger)] == ' ' or len(' '.join(message)) == len(trigger)-1:
        return None

    print(' '.join(message)[len(trigger)])
    if channel in settings['connections'][con.network]['ignore_suffix'] and ' '.join(message)[len(trigger)] in settings['connections'][con.network]['ignore_suffix'][channel]:
        return

    if channel == con.nickname:
        channel = user.split('!')[0][1:]

    m_string = ' '.join(message)[1:]
    for t in trigger:
        if m_string.startswith(t):
            cmd_string = m_string[len(t):]
            command = cmd_string.split(' ')[0]
            if len(cmd_string.split(' ')) > 1:
                params = [x for x in cmd_string.split(' ')[1:] if x != '']
            else:
                params = []
            
            command_list = build_commandlist(channel, con.network, user)

            for cmd in command_list:
                aliases = getattr(command_list[cmd], 'aliases', None)
                if aliases is None:
                    continue
                for alias in aliases:
                    if alias == command:
                        command = cmd

            if command not in command_list:
                if channel in settings['connections'][con.network]['default_commands']:
                    command = settings['connections'][con.network]['default_commands'][channel]
                    func = getattr(command_list[command], command)
                    params = [x for x in cmd_string.split(' ')]
                else:
                    con.privmsg(channel, '\x034Could not find that command.\x03')
                    return None
            else:
                func = getattr(command_list[command], command)

            sig = inspect.signature(func)
            prms = sig.parameters
            optional = 0
            required = 0

            for i, p in enumerate(prms):
                if i < 6:
                    continue

                if (prms[p].default == prms[p].empty and 
                        prms[p].kind != prms[p].VAR_POSITIONAL):
                    required += 1
                else:
                    optional += 1

            if (len(params) > (required+optional) and not any(prms[p].kind == 
                    prms[p].VAR_POSITIONAL for p in prms) or
                    len(params) < required):
                output = ('Invalid params: Command "{}{}" has {} required '
                          'params and {} optional params. You gave {} '
                          'params.').format(t, command, required, optional,
                          len(params))
            else:

                try:
                    output = func(con, globals(), command_list, t, user, 
                                  channel, *params)
                except Exception as error:
                    output = str(error)

            if output is None:
                return None
            if isinstance(output, list):
                for line in output:
                    con.privmsg(channel, line)
            else:
                con.privmsg(channel, output)
    return None


def build_commandlist(channel, network, host):
    cmdlist = {}
    for cl in commands:
        for ch in cl.split(','):
            if ch == '__all__':
                for c in commands[cl]:
                    cmdlist[c] = commands[cl][c]

            owners = settings['connections'][network]['owners']
            if ch == 'owner' and any(o in host for o in owners):
                for c in commands[cl]:
                    cmdlist[c] = commands[cl][c]

            if not ch.startswith('!') and ch == channel or not channel.startswith('#'):
                for cmd in commands[cl]:
                    cmdlist[cmd] = commands[cl][cmd]
            
            if ch.startswith('!') and ch[1:] != channel or not channel.startswith('#'):
                for cmd in commands[cl]:
                    cmdlist[cmd] = commands[cl][cmd]
    return cmdlist


def load_commands():
    global commands
    channels = os.listdir('commands/')
    for channel in channels:
        if not os.path.isdir('commands/{}'.format(channel)):
            continue
        files = os.listdir('commands/{}'.format(channel))
        commands[channel] = {}
        for f in files:
            if not f.endswith('.py'):
                continue
            if os.path.isfile('commands/{}/{}'.format(channel, f)):
                name = f.replace('.py', '')
                src = imp.load_source('{}_{}'.format(channel, name),
                                      'commands/{}/{}'.format(channel, f))
                commands[channel][name] = src
    return None


def load_plugins():
    global plugins
    files = os.listdir('plugins/')
    for filename in files:
        if not filename.endswith('.py'):
            continue
        name = filename.split('.py')[0]
        src = imp.load_source('plugin_{}'.format(filename), 'plugins/{}'.format(filename))
        plugins[filename] = src
    return None


def load_settings():
    global settings
    with open('settings.json') as sfile:
        settings = json.loads(sfile.read())
    return None


@threads.asthread()
def reload_loop(delay=60):
    while True:
        load_commands()
        load_settings()
        load_plugins()
        time.sleep(delay)
    return None


def url_download(url):
    request = urllib.request.urlopen(url)
    response = request.read()
    try:
        decoded = response.decode('utf-8')
    except UnicodeDecodeError:
        return None
    return decoded


def main():
    global connections
    load_commands()
    load_settings()
    load_plugins()
    reload_loop()

    for connection in settings['connections']:

        # Checks if the user has specified to run the connection.
        if not settings['connections'][connection]['running']:
            continue
        
        irc_connection = base.Connection(connection, settings['connections']
                         [connection]['port'])
        irc_connection.set_ident('sjBot')
        irc_connection.set_handler(base.handler, globals())
        #rc_connection.display_func = interface.display

        connected = irc_connection.connect()

        if connected:
            connections[irc_connection.network] = irc_connection
            irc_connection.identify()
            irc_connection.receive_loop()
    return None


if __name__ == '__main__':
    #interface = simple_ui.Interface(ui_message)
    #interface.handle_input()
    main()