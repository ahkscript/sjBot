import urllib.request
import html.parser
import re
import xml.etree.ElementTree as ET
meta_data 	= { "help": ["Requests information from Wolfram Alpha", "&botcmdwolfram <query>"], "aliases": ["wolfram", "wa"], "owner": 0 }

def execute(parent, commands, user, host, channel, params):
	if len(params ) == 0:
		return ["This command needs more params"]

	url = 'http://api.wolframalpha.com/v2/query?input=' + '%20'.join( params ) + "&appid=" + parent.keys['wolfram']
	htmlData = parent.download_url( url )
	root = ET.fromstring(htmlData)
	items = root.findall('.//subpod')
	if len(items) == 0:
		return 'No data found!'
	try:
		output = items[0][0].text + ' - ' + items[1][0].text
	except:
		return 'No data found!'
	return output
