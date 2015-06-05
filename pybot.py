#!/urs/bin/env python3
import sys
import time
import random
import math
import cmath
from bot import bot


def p(data, end='\r\n'):
    socket.send(b'PRIVMSG #Sjc_Bot :' + bytes(str(data) + end, 'utf-8'))
    return None

def help():
    return 'Python sandbox through IRC!! YAAAAY!!'

socket = None
globa = {'__builtins__': {'time': time, 'random': random, 'range': range, 
        'math': math, 'abs': abs, 'all': all, 'any': any, 'ascii': ascii, 
        'bin': bin, 'bool': bool, 'bytearray': bytearray, 'bytes': bytes, 
        'callable': callable, 'chr': chr, 'classmethod': classmethod, 
        'complex': complex, 'dir': dir, 'dict': dict, 'divmod': divmod, 
        'enumerate': enumerate, 'filter': filter, 'float': float, 
        'format': format, 'frozenset': frozenset, 'getattr': getattr, 
        'deleteattr': delattr, 'hasattr': hasattr, 'hash': hash, 'hex': hex, 
        'id': id, 'int': int, 'isinstance': isinstance, 
        'issubclass': issubclass, 'iter': iter, 'len': len, 'list': list, 
        'map': map, 'max': max, 'min': min, 'next': next, 'object': object, 
        'oct': oct, 'ord': ord, 'pow': pow, 'property': property, 
        'repr': repr, 'reversed': reversed, 'round': round, 'set': set, 
        'setattr': setattr, 'slice': slice, 'sorted': sorted, 
        'staticmethod': staticmethod, 'str': str, 'sum': sum, 'tuple': tuple, 
        'type': type, 'zip': zip, 'exit': exit, 'help': help, 'cmath': cmath, 
        'print': p}}
local = {}


class pybot(bot):
    
    remove = ['import']
    more = ''
    want_more = False
    owners = ['c/kiwiirc.com/ip.180.181.27.230']

    def __init__(self):
        global socket
        bot.__init__(self, 'irc.freenode.net', 6667)
        socket = self.irc
        self.main_loop()
    
    def startup(self):
        self.nickname = 'sjPythonBot'
        self.user = 'Sjc1000'
        self.host = 'Sjc1000'
        self.realname = 'Uptone-Software'
        self.ident()
        return None
    
    def on376(self, *params):
        self.send('PRIVMSG Nickserv :identify Sjc1000 a1b2c3d4e5')
        return None
    
    def on396(self, *host):
        self.join('#Sjc_Bot')
        return None
    
    def onJOIN(self, host, channel):
        if self.nickname not in host:
            return None

        if channel == '#Sjc_Bot':
            self.privmsg(channel, 'Python 3.3.1 (default, Sep 25 2013, '
                '19:29:01)')
            self.privmsg(channel, 'Uptone-Software python sandbox. Some '
                'features have been disabled.')
        return None
    
    def execute(self, data, channel):
        global local
        try:
            exec(data, globa, local)
        except SystemExit:
            return None
        except:
            self.privmsg(channel, 'Error : ' + str(sys.exc_info()[0]) + ' ' + 
                  str(sys.exc_info()[1]))
        return None
        
    def onPRIVMSG(self, host, channel, *message):
        global local
        local = {}
        if any(x in host for x in self.owners):
            print('Owner')
            local['irc'] = self
        join = ' '.join(message)
        join = join[1:]
        if join.startswith('>>> '):
            join = join.replace('>>> ', '')
            self.execute(join, channel)
            return None
        print('|' + join + '|')
        if join in ['>>>>', '>>>> ']:
            print('execute')
            self.execute(self.more, channel)
            self.more = ''
        if join.startswith('>>>> '):
            join = join.replace('>>>> ','')
            self.more += '\n' + join
        return None

if __name__ == '__main__':
    pb = pybot()          
