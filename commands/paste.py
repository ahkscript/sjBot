meta_data 	= { "help": ["Tells a user to use a pastebin.","Usage: &botcmdpaste"], "aliases": ["p", "paste"], "owner": 0 }

# url http://ahk.uk.to/
def execute(parent, command, user, host, channel, params ):
	if channel == "#ahk":
		url = "http://ahk.us.to/"
	else:
		url = "http://ahk.uk.to/"
	return {'Status': 0, 'Text': "Please paste your code at the unofficial AutoHotkey pastebin: " + url, 'Error': 'No Error'}
