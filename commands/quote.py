import urllib.request
import json

meta_data = { "help": ["Says a random quote.","Usage: &botcmdquote"], "aliases": ["q", "quote"], "owner": 0 }

def execute(parent, commands, user, host, channel, params):
	jdata = parent.download_url('http://www.iheartquotes.com/api/v1/random?format=json&max_lines=1')
	data = json.loads(jdata)
	return [data['quote'] + ' ~ ' + data['source']]
	
