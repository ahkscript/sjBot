import urllib.request
import json
import time

def urlDownload( url ):
	try:
		response 	= urllib.request.urlopen(url) 
	except UnicodeEncodeError:
		return -1
	except:
		return -2
	return response.read().decode('utf-8')

def on376(this, params):
	old_events = ['']
	while True:
		data = urlDownload('https://api.github.com/users/ahkscript/events')
		events = json.loads(data)
		if old_events != [''] and old_events != events:
			event_data = [x for x in events if x not in old_events]
			for ev in event_data:
				send_data = globals()[ev['type']](ev)
				this.irc.privmsg('#ahkscript', '[ Github ] ' + send_data)
		old_events = events
		time.sleep(30)

def PushEvent(event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	size = event_data['payload']['size']
	if size > 1:
		output = ' commits'
	else:
		output = ' commit'
	url = event_data['repo']['url']
	return user + ' pushed ' + str(size) + output + ' to ' + repo + ' - ' + url

def IssuesEvent(event_data):
	user = event_data['actor']['login']
	action = event_data['payload']['action']
	name = event_data['payload']['issue']['title']
	return user + ' ' + action + ' the issue: ' + name

def IssueCommentEvent(event_data):
	user = event_data['actor']['login']
	name = event_data['payload']['issue']['title']
	return user + ' commented on the issue: ' + name

def WatchEvent(event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	return user + ' starred ' + repo

def CreateEvent(event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	ctype = event_data['payload']['ref_type']
	message = event_data['payload']['description']
	return user + ' created a ' + ctype + ' at ' + repo + ' :' + message
