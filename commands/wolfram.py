import urllib.request
import html.parser
import re
meta_data 	= { "help": ["Searches google for an ahk related query.","Usage: &botcmdahk <query>"], "aliases": ["wolfram", "wa"], "owner": 0 }

def execute(parent, command, user, host, channel, params ):
	if len(params ) == 0:
		return "This command needs more params"

	url 		= 'http://api.wolframalpha.com/v2/query?input=' + '%20'.join( params ) + "&appid=" + parent.keys['wolfram']
	htmlData	= parent.download_url( url )
	try:		
		res 			= re.findall('<plaintext>(.*?)</plaintext>', htmlData )
		return {'Status': 0, 'Text': "\x02" + res[0] + "\x02 - " + html.parser.HTMLParser().unescape( res[1]).decode("utf-8"), 'Error': 'No Error'}
	except:
		return {'Status': 0, 'Text': "\x02No Results Found!\x02", 'Error': 'No Error'}
