import re
import urllib.request
import json


def onPRIVMSG(this, *message):
	reg = re.search("watch\?v=(.*?)(\&|\s+|$|#)", ' '.join( message[3:] ) )
	try:	
		url = reg.group(1)
	except AttributeError:
		return 0

	rep = re.findall('\&(\w+)',' '.join(message[3:]))

	youtubedata = this.download_url( 'https://www.googleapis.com/youtube/v3/videos?id=' + url + '&key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&part=snippet,contentDetails,statistics,status' )
	response = json.loads( youtubedata )
	time = response['items'][0]['contentDetails']['duration'][2:].replace("M", ":").replace("S", "").replace("H", ":").split(":")
	for index, val in enumerate(time):
		time[index] = '%02d' % (int(val),)
	output = '[' + message[0].split("!")[0][1:] + "'s link] " + response['items'][0]['snippet']['title'] + " - " + ':'.join(time)
	
	for x in rep:
		try:
			output = output + " - " + x + ": " + response['items'][0]['statistics'][x]
		except AttributeError:
			pass
	print( output )
	this.privmsg(message[2], output )
