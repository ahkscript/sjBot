#!/usr/bin/env python3


import json
import re
import difflib


meta_data = {'help': ['Shows information about AutoHotkey commands.', '&botcmdinfo <command>'], 'owner': 0, 'aliases': ['inf', 'info', 'ahk_info']}

def execute(sjBot, commands, user, host, channel, params):
	if len(params) < 1:
		return 'This command needs more params.'

	with open(sjBot.def_dir + '/commands/docs.json', 'r') as file:
		docs = json.loads(file.read())

	match = difflib.get_close_matches(' '.join(params), docs)
	
	if len(match) == 0:
		return 'Could not find information for that command.'
	command = match[0]
	html_data = sjBot.download_url(docs[command])
	matches = re.search('<p>(.*?)</p>.*?<pre class="Syntax">(.*?)</pre>', html_data, re.S)
	desc = matches.group(1)
	example = matches.group(2)
	desc = repl = re.sub('<.*?>', '', desc)
	return ['\x02{}\x02 - {} - {}'.format(params[0], sjBot.html_decode(desc), docs[command]), sjBot.html_decode(example)]