

import urllib.request
import urllib.parse
import re


def onPRIVMSG(this, full_host, p, channel, *message):
    if message[0] in [':' + this.nickname + ':', '>', '|']:
        data = this.download_url(message[1])
        p = re.compile(r'<title>(.*?)</title>')
        match = re.search(p, data)
        try:
            title = match.group(1)
        except AttributeError:
            return None
        this.privmsg(channel, urllib.parse.unquote( title ))
    return None
