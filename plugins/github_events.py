import urllib.request
import json
import time
import os


def urlDownload( url ):
	try:
		response 	= urllib.request.urlopen(url) 
	except UnicodeEncodeError:
		return -1
	except:
		return -2
	return response.read().decode('utf-8')

def on001(this, params):
	with open(os.path.dirname(os.path.realpath(__file__)) + '/old_events', 'w') as my_file:
		my_file.write( urlDownload(repo + access_token) )

def onUPDATE(this, params):
	with open(os.path.dirname(os.path.realpath(__file__)) + '/old_events', 'r') as my_file:
		try:
			old_events = json.loads( my_file.read() )
		except ValueError:
			print('! Error with loading events file. Waiting until it contains json data.')
			with open(os.path.dirname(os.path.realpath(__file__)) + '/old_events', 'w') as my_file:
				download_data = urlDownload(repo + access_token)
				my_file.write( download_data )
			return -1

	data = urlDownload(repo + access_token)
	events = json.loads(data)
	if old_events != [''] and old_events != events:
		event_data = [x for x in events if x not in old_events]
		for ev in event_data:
			try:
				send_data = globals()[ev['type']](ev)
			except KeyError:
				return -1
			this.irc.privmsg('#ahkscript', '[GitHub] ' + send_data)
			time.sleep(1)
		
	with open(os.path.dirname(os.path.realpath(__file__)) + '/old_events', 'w') as my_file:
		my_file.write(json.dumps(events))

def PushEvent(event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	size = event_data['payload']['size']
	message = event_data['payload']['commits'][0]['message']
	message = message[:50]
	message = message.replace('\n', '--')
	if size > 1:
		return user + ' pushed ' + str(size) + ' commits to ' + repo
	else:
		return user + ' pushed ' + str(size) + ' commit to ' + repo + ' - ' + message

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
	message = message[:50]
	message = message.replace('\n', '--')
	return user + ' created a ' + ctype + ' at ' + repo + ' - ' + message

def PullRequestEvent(event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	action = event_data['payload']['action']
	message = event_data['payload']['pull_request']['title']
	message = message[:50]
	message = message.replace('\n', '--')
	return user + ' ' + action + ' a pull request to ' + repo + ' - ' + message

with open(os.path.dirname(os.path.realpath(__file__)) + '/access_token', 'r') as my_file:
	access_token = my_file.read()

repo = 'https://api.github.com/users/ahkscript/events?access_token='
