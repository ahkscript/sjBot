import urllib.request
import json
import time
import os

def on001(this, params):
	with open(this.plugins_dir + 'old_events', 'w') as my_file:
		my_file.write( this.download_url(repo + this.keys['github']) )

def onUPDATE(this, params):
	with open(this.plugins_dir + 'old_events', 'r') as my_file:
		try:
			old_events = json.loads( my_file.read() )
		except ValueError:
			print('! Error with loading events file. Waiting until it contains json data.')
			with open(this.plugins_dir +  'old_events', 'w') as my_file:
				download_data = this.download_url(repo + this.keys['github'])
				my_file.write( download_data )
			return -1

	data = this.download_url(repo + this.keys['github'])
	events = json.loads(data)
	if old_events != [] and old_events != events:
		event_data = [x for x in events if x not in old_events]
		for ev in event_data:
			try:
				send_data = globals()[ev['type']](this, ev)
			except KeyError:
				return -1
			this.irc.privmsg('#ahkscript', '[GitHub] ' + send_data)
			time.sleep(1)
		
	with open(this.plugins_dir + 'old_events', 'w') as my_file:
		my_file.write(json.dumps(events))

def PushEvent(this, event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	size = event_data['payload']['size']
	message = event_data['payload']['commits'][0]['message']
	message = message[:50]
	message = message.replace('\n', '--')
	url = event_data['payload']['commits'][0]['url'].replace('https://api.github.com/repos/', 'https://github.com/')
	if size > 1:
		return user + ' pushed ' + str(size) + ' commits to ' + repo
	else:
		return user + ' pushed ' + str(size) + ' commit to ' + repo + ' - ' + message + ' - ' + this.shorten_url(url)

def IssuesEvent(this, event_data):
	user = event_data['actor']['login']
	action = event_data['payload']['action']
	repo = event_data['repo']['name']
	name = event_data['payload']['issue']['title']
	url = event_data['payload']['issue']['html_url']
	return user + ' ' + action + ' the issue "' + name + '" at ' + repo + ' - ' + this.shorten_url(url)

def IssueCommentEvent(this, event_data):
	user = event_data['actor']['login']
	name = event_data['payload']['issue']['title']
	repo = event_data['repo']['name']
	url = event_data['payload']['issue']['html_url']
	return user + ' commented on the issue "' + name + '" at ' + repo + ' - ' + this.shorten_url(url)

def WatchEvent(this, event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	return user + ' starred ' + repo

def CreateEvent(this, event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	ctype = event_data['payload']['ref_type']
	url = event_data['payload']['repository']['html_url']
	message = event_data['payload']['description']
	message = message[:50]
	message = message.replace('\n', '--')
	return user + ' created a ' + ctype + ' at ' + repo + ' - ' + message + ' - ' + this.shorten_url(url)

def PullRequestEvent(this, event_data):
	user = event_data['actor']['login']
	repo = event_data['repo']['name']
	action = event_data['payload']['action']
	url = event_data['payload']['pull_request']['html_url']
	message = event_data['payload']['pull_request']['title']
	message = message[:50]
	message = message.replace('\n', '--')
	return user + ' ' + action + ' a pull request to ' + repo + ' - ' + message + ' - ' + this.shorten_url(url)

repo = 'https://api.github.com/users/ahkscript/events?access_token='
