#!/usr/bin/env python3
'''
    sjBot is a Python IRC Bot made by Sjc1000 ( Steven J. Core )
            Copyright © 2015, Steven J. Core
    
    sjBot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


from os import listdir
import imp
import json
import os
import sys
import threading
import time
import urllib.request
import html.entities
from cprint import cprint
from base import base
from threads import asthread


def timestamp():
    time_object = time.localtime(time.time())
    return '[{:0>2}:{:0>2}:{:0>2}]'.format(time_object[3],
              time_object[4],time_object[5])


class sjBot(base):

    last_user = None

    def __init__(self, keyfile='keys'):
        """__init__
        Loads all the plugins and initiates the bot class.
        It then starts the main_loop()
        """
        self.def_dir = os.path.dirname(os.path.realpath(__file__))
        with open(self.def_dir + '/' + keyfile, 'r') as my_file:
            self.keys = json.loads( my_file.read() )
        self.getsettings()
        self.display('Loading commands and plugins.')
        self.commands = self.load_plugins(self.def_dir + '/commands/')
        self.plugins = self.load_plugins(self.def_dir + '/plugins/')
        self.display('Connecting to IRC.')
        base.__init__(self, self.network, self.port)
    
    def getsettings(self):
        """getsettings
        Loads the settings from the .json file. Tells you if you're missing
            a required setting.
        """
        with open(self.def_dir + '/sjbot.settings','r') as mfile:
            data = mfile.read()
            settings = json.loads(data)
        required = ['creds','nickname','user','host','realname','network',
                    'port','channel_list','default_cmd','botcmd','ignore',
                    'ownerlist']
        for check in required:
            if check not in settings:
                self.display('[.red]Setting missing: [.yellow]' + check)
                sys.exit(0)
                return 0
        for key in settings:
            setattr(self, key, settings[key])
        return None
    
    def onSTARTUP(self):
        """onSTARTUP
        Called when the bot starts. This function usually contains the 
            .connect() method of the base class.
        This then calls the iterate function in another thread,
            this allows sjBot to reload data on the fly.
        """
        self.display('Startup initiated.')
        connected = self.connect()
        if connected is False:
            self.display('[.red] Could not connect to the network.')
            return None
        self.identify(self.nickname, self.user, self.host, self.realname)
        iterate_thread = threading.Thread(target=self.iterate)
        iterate_thread.daemon = True
        iterate_thread.start()
        return None
    
    def iterate(self, timeout=60):
        """iterate
        Reloads most of the data. Giving sjBot the ability to update without
            having to disconnect from IRC.
        """
        while True:
            with open(self.def_dir + '/sjbot.settings') as settings:
                settings = json.loads(settings.read())
            self.botcmd = settings['botcmd']
            self.ownerlist = settings['ownerlist']
            self.ignore = settings['ignore']
            self.default_cmd = settings['default_cmd']
            self.commands = self.load_plugins(self.def_dir + '/commands/')
            self.plugins = self.load_plugins(self.def_dir + '/plugins/')
            time.sleep(timeout)
        return None
    
    def start_monitor(self):
        """start_monitor
        Starts the user monitor, sending a list of users to IRC to monitor.
        IRC returns data when they are online / offline. sjBot handles them
            in on730 and on731.
        """
        self.display('[.yellow] Starting user monitor.')
        with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
            monitor_list = json.loads(mfile.read())
        users = []
        
        for musers in monitor_list:
            for us in monitor_list[musers]:
                if us not in users:
                    users.append(us)
        for us in users:
            self.send('MONITOR + ' + us)
        self.display('Monitoring users: ' + ', '.join(users))
        return None
    
    def load_plugins(self, plugin_folder):
        """load_plugins
        Loads all the commands and plugins. Using the imp library.
        """
        plugins = {}
        files = listdir(plugin_folder)
        for f in files:
            if not f.endswith('.py'):
                continue
            name = f[:f.index('.')]
            plugins[name] = imp.load_source('pl_' + name, plugin_folder  + f)
        return plugins
    
    def shorten_url(self, url):
        """shorten_url
        shorten's a URL. This function is accessible by every command.
        """
        response = self.download_url('https://api-ssl.bitly.com/v3/shorten?'
                                     'access_token=' + self.keys['bitly'] + 
                                     '&format=txt&Longurl=' + url)
        if response is False:
            return url
        return response
    
    def download_url(self, url):
        """download_url
        Downloads a URL. This function is accessible by every command.
        """
        try:
            response = urllib.request.urlopen(url)
        except:
            return False
        return response.read().decode('utf-8')

    def google(self, query):
        response = self.download_url('https://ajax.googleapis.com/ajax/'
            'services/search/web?v=1.0&q=' + '%20'.join(query.split(' ')))
        return response

    def html_decode(self, data):
        for char in html.entities.html5:
            if '&' + char + ';' in data:
                data = data.replace('&' + char + ';', 
                                    html.entities.html5[char])
        return data
    
    @asthread(True)
    def onALL(self, *params):
        """onALL
        This is called on every type of IRC message.
        This then finds if any plugins have the message and calls them.
        """
        mtype = params[1]
        
        for pl in self.plugins:
            if hasattr(self.plugins[pl], 'on' + mtype):
                function = getattr(self.plugins[pl], 'on' + mtype)
                function(self, *params)
        return None
    
    @asthread(True)
    def on730(self, host, nickname, ohost):
        """on730
        Called when a user that is being watched comes online.
        If anyone has specified they want to see this data, it shows them.
        """
        if nickname == self.nickname:
            return 0
        
        user = ohost.split('!')[0][1:]
        uhost = ohost.split('!')[1]
        
        with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
            monitor_list = json.loads(mfile.read())
        for notify in monitor_list:
            for us in monitor_list[notify]:
                if us == user:
                    self.notify(notify,'*** ' + us + ' is online ***')
        return None
    
    @asthread(True)
    def on731(self, host, nickname, ohost):
        """on731
        Called when a user that is being watched goes offline.
        If anyone has specified that they want to see this data, it shows them.
        """
        if nickname == self.nickname:
            return 0
        
        user = ohost[1:]
        
        with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
            monitor_list = json.loads(mfile.read())
        for notify in monitor_list:
            for us in monitor_list[notify]:
                if us == user:
                    self.notify(notify,'*** ' + us + ' is offline ***')
        return None
    
    @asthread(True)
    def on433(self, host, ast, nickname, *params):
        """on433
        Called when the nickname sjBot tries to use is already being used.
        He will append _ to the end and try again.
        
        *note to self* 
        Future updates should use a numbering system.
        """
        self.nickname = nickname + '_'
        self.send('NICK ' + self.nickname)
        self.display('Nickname already taken. Trying again with ' + 
                     self.nickname)
        return None
    
    @asthread(True)
    def on376(self, host, *params):
        """on376
        End of MOTD messages.
        sjBot will now attempt to log_datain to freenode's nickserv.
        """
        username = self.creds['username']
        password = self.creds['password']
        self.send('PRIVMSG Nickserv :Identify ' + username + 
                  ' ' + self.keys[password])
        self.display('[.yellow] Sending credentials to NickServ.')
        return None
    
    @asthread(True)
    def on396(self, host, chost, *params):
        """on396
        sjBot successfully logged into freenode. He will now join the channels
            in self.channel_list
        He will also start the user monitor system.
        """
        for channel in self.channel_list:
            self.join(channel)
        self.display('Joining channels.')
        self.start_monitor()
        return None

    @asthread(True)
    def onKICK(self, host, channel, *junk):
        """onKICK
        rejoins a channel when he has been kicked.
        """
        self.join(channel)
        return None

    @asthread(True)
    def onINVITE(self, host, botname, channel, *junk):
        """onINVITE
        When someone invites the bot to a channel.
        """
        self.queue.append({'function': self.privmsg, 'params': (channel[1:],
            'You wanted to see me? ;)'), 'event': 'JOIN'})
        self.join(channel)
        return None
    
    @asthread(True)
    def onPRIVMSG(self, uhost, channel, *message):
        """onPRIVMSG
        Happens when anyone talks in either the channel or PM.
        sjBot checks for a command, and does all the command stuff then will
            return any data given by the command.
        """
        self.load_plugins(self.def_dir + '/commands/')
        user, host = uhost.split('!')
        user = user[1:]
        self.last_user = user
        message = [x for x in message]
        message = [message[0][1:]] + message[1:]
        
        if channel in self.botcmd:
            botcmd = self.botcmd[channel]
        else:
            botcmd = self.botcmd['default']
        
        if isinstance(botcmd, list):
            check = botcmd
            for bt in check:
                if message[0].startswith(bt):
                    botcmd = bt
                    break
        if not isinstance(botcmd, list):
            command = message[0][len(botcmd):]
            
            if any(command.startswith(c) for c in self.ignore):
                return 0
            params = message[1:]
            
            cmd = self.is_command(command.lower())
            
            if cmd == 0:
                if channel in self.default_cmd:
                    cmd = self.default_cmd[channel]
                else:
                    cmd = self.default_cmd['default']
                params = [message[0][len(botcmd):]] + message[1:]

            if channel == self.nickname:
                channel = user
            self.display('Command ' + command + ' received')
            if self.commands[cmd].meta_data['owner'] == 1 and not any(us in 
                    uhost for us in self.ownerlist):
                self.privmsg(channel, 'You do not have permission to use '
                             'that!')
                return 0
            
            response = self.commands[cmd].execute(self, self.commands, user, 
                                                  host, channel, params)
            if response == 0:
                return 0
            if isinstance(response, int):
                response = [str(response)]
            if isinstance(response, str):
                response = [response]
            for re in response:
                self.privmsg(channel, re.replace('&botcmd', botcmd))
        return 0

    def display(self, data):
        cprint(data, '[.purple]' + timestamp() + '[./purple] ')
        return None
    
    def is_command(self, command):
        """is_command
        Checks if a command is known to the bot. It also checks the aliases.
        If it is known, it will return the command name.
        If its an alias, it will return the real name of the command.
        """
        for cm in self.commands:
            if any(command == c for c in self.commands[cm].meta_data[
                   'aliases']):
                return cm
        return False

def main():
    main = sjBot()

    try:
        cprint('[.green]Starting main loop.', '[.purple]' + timestamp() + 
               '[./purple] ')
        main.main_loop()
    except KeyboardInterrupt:
        print('')
        cprint('[.red]Received the command to shutdown.', '[.purple]' + 
               timestamp() + '[./purple] ')
        main.shutdown()
    except:
        cprint('[.red] Something went wrong.', '[.purple]' + timestamp() + 
               '[./purple] ')
        raise
    return None


if __name__ == '__main__':
    main()