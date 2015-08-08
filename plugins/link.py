

import urllib.request
import urllib.parse
import re


def onPRIVMSG(this, full_host, p, channel, *message):
    if message[0][1:] in [':' + this.nickname + ':', '>', '|']:
        data = this.download_url(message[1])
        print( data )
        p = re.compile(r'<title>(.*?)</title>')
        match = re.search(p, data)
        print( match )
        try:
            title = match.group(1)
        except AttributeError:
            return None

        nickname = full_host.split('!')[0][1:]
        this.privmsg(channel, '[' + nickname + "'s link] " + urllib.parse.unquote( title ))
    return None
