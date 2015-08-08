

import re
import urllib.request
import json


def onPRIVMSG(this, host, privmsg, channel, *message):
	reg = re.search("(yout.*v=|yout.*/)(.*?)(\&|\s+|$|#)", ' '.join( message ) )
	try:	
		url = reg.group(2)
	except AttributeError:
		return 0

	youtubedata = this.download_url( 'https://www.googleapis.com/youtube/v3/videos?id=' + url + '&key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&part=snippet,contentDetails,statistics,status' )
	
	response = json.loads( youtubedata )
	time = response['items'][0]['contentDetails']['duration'][2:].replace("M", ":").replace("S", "").replace("H", ":").split(":")
	
	for index, val in enumerate(time):
		time[index] = '%02d' % (int(val),)
	
	output = '[' + host.split("!")[0][1:] + "'s link] " + response['items'][0]['snippet']['title'] + " - " + ':'.join(time)
	

	if '|' in message:
		rep = ['likeCount', 'dislikeCount', 'viewCount'] + message[message.index('|')+1:]
	else:
		rep = ['likeCount', 'dislikeCount', 'viewCount']

	for x in rep:
		try:
			output = output + " - " + x + ": " + response['items'][0]['statistics'][x]
		except AttributeError:
			pass
	print( output )
	this.privmsg(channel, output )
	return None