

import time
import urllib.request
import os
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import socket
from cprint import cprint
from base import base
from threads import asthread


feed_url = 'http://www.autohotkey.com/board/rss/forums/2-'


def html_decode(data):
    """html_decode
    Decodes the html characters from a string
    """
    for char in html.entities.html5:
        if '&' + char + ';' in data:
            data = data.replace('&' + char + ';', 
                                html.entities.html5[char])
    return data


def download_url(url):
    """download_url
    Downloads a URL. This function is accessible by every command.
    """
    try:
        response = urllib.request.urlopen(url)
    except:
        return False
    return response.read().decode('utf-8')


class htmlStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.data = []
        self.prepend = []
    
    def handle_data(self, data):
        self.data.append(data)
    
    def get_data(self):
        return ''.join(self.data)


def strip(html, item):
    if 'author' in item.tag:
        if len(item):
            return item[0].text
    s = htmlStripper()
    if html == None:
        return None
    s.feed(html)
    return s.get_data()


def strbrackets(data):
    if '}' in data:
        return data[data.find('}')+1:]
    return data


def parse(data):
    root = ET.fromstring(data)
    items = root.findall('.//item')
    if len(items) == 0:
        items = []
        for i in root:
            if 'entry' in i.tag:
                items.append(i)
    output = []
    for child in items:
        output.append({strbrackets(i.tag):strip(i.text, i) for i in child})
    return output


class ahkbot(base):

    network = 'irc.freenode.net'
    port = 6667
    nickname = 'ahkbot'
    user = 'sjBot'
    host = 'sjBot'
    realname = 'Uptone-Software/ahkbot'
    channel = '#Sjc_Bot'


    def __init__(self):
        with open('keys', 'r') as keyfile:
            self.keys = json.loads(keyfile.read())
        print( self.keys )
        base.__init__(self, self.network, self.port, self.nickname, self.user,
                      self.host, self.realname)

    def onSTARTUP(self):
        connected = self.connect()
        if connected is False:
            self.display('Could not connect.')
            return None
        return None

    def display(self, data, color='purple'):
        cprint('[.' + color + ']' + data)
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
        username = 'sjBot'
        password = self.keys['sjbot_pass']
        self.display('Sending credentials to NickServ.')
        self.send('PRIVMSG Nickserv :Identify ' + username + 
                  ' ' + password)
        return None

    def on396(self, *junk):
        self.join(self.channel)
        return None

    def onJOIN(self, host, channel, *junk):
        print( host.split('!')[0] )
        if host.split('!')[0][1:] == self.nickname:
            self.feed_loop()
        return None

    @asthread(True)
    def feed_loop(self):
        previous = None
        current = None

        while True:
            feed = download_url(feed_url)
            current = parse(feed)
            
            if previous == None:
                previous = current
                continue

            difference = [x for x in current if x not in previous]
            if len(difference) > 0:
                print( difference )

            print('End loop')
            time.sleep(10)
            #time.sleep(60)
        return None


def main():
    program = ahkbot()
    program.main_loop()
    return None

if __name__ == '__main__':
    main()