import bot
import json
import urllib.request
import os
import re
import time


class AutoGitBot(bot.ircBot):
	nickname = 'AutoGitBot'
	repo = 'https://api.github.com/users/ahkscript/events?access_token='
	def __init__(self, network, port, keyfile='keys'):
		self.def_dir = os.path.dirname(os.path.realpath(__file__))
		with open(self.def_dir + '/' + keyfile, 'r') as my_file:
			self.keys = json.loads( my_file.read() )
		self.def_dir = os.path.dirname(os.path.realpath(__file__))
		self.irc = bot.ircBot(network, port, self)
		self.irc.ident(self.nickname, self.nickname, self.nickname, 'Uptone Software')
		with open(self.def_dir + '/old_events', 'w') as mfile:
			mfile.write( self.download_url(self.repo + self.keys['github']) )
		self.irc.data_loop()

	def on433(self, host, ast, nickname, *params):
		self.irc.send('NICK ' + nickname + '_')
		self.nickname = nickname + '_'
		return 0
	
	def on376(self, host, *params):
		self.irc.send('PRIVMSG NickServ :Identify AutoGitBot ' + self.keys['sjbot_pass'], star=self.keys['sjbot_pass'])
		return 0
	
	def on396(self, host, chost, *params):
		self.irc.join('#ahkscript')
		
		with open(self.def_dir + '/old_events', 'w') as wfile:
			data = self.download_url(self.repo + self.keys['github'])
			wfile.write(data)
		
		self.irc.iterate()
		return 0
	
	def shorten_url(self, url):
		response = self.download_url('https://api-ssl.bitly.com/v3/shorten?access_token=' + self.keys['bitly'] + '&format=txt&Longurl=' + url)
		if response == 0:
			return url
		return response
	
	def download_url(self, url):
		try:
			response 	= urllib.request.urlopen(url) 
		except UnicodeEncodeError:
			return 0
		except:
			return 0
		return response.read().decode('utf-8')
	
	def onITERATE(self):
		with open(self.def_dir + '/old_events', 'r') as mfile:
			try:
				old_events = json.loads( mfile.read() )
			except ValueError:
				print('! No json data in old events. Downloading some.')
				with open(self.def_dir + '/old_events', 'w') as wfile:
					data = self.download_url(self.repo + self.keys['github'])
					wfile.write(data)
				return -1
		
		data = self.download_url(self.repo + self.keys['github'])
		new_data = json.loads(data)
		if old_events != new_data:
			event_data = [x for x in new_data if x not in old_events]
			for ev in event_data:
				if hasattr(self, ev['type']):
					func = getattr(self, ev['type'])
					data = func(ev)
					self.irc.privmsg('#ahkscript', data)
					
			with open(self.def_dir + '/old_events', 'w') as wfile:
					wfile.write(json.dumps(new_data))
		return 0

	def PushEvent(self, e):
		user = e['actor']['login']
		size = e['payload']['size']
		repo = e['repo']['name']
		url = self.shorten_url('https://github.com/' + e['repo']['name'] + '/commits/master')
		message = e['payload']['commits'][0]['message'][:20]
		return user + ' pushed ' + str(size) + ' commit[s] to ' + repo + ' ' + message + ' - ' + url
	
	def IssueEvent(self, e):
		user = e['actor']['login']
		action = e['payload']['action']
		repo = e['repo']['name']
		url = self.shorten_url(e['payload']['issue']['html_url'])
		title = e['payload']['issue']['title'][:20]
		return user + ' ' + action + ' the issue at ' + repo + ' ' + title + ' - ' + url
	
	def ForkEvent(self, e):
		user = e['actor']['login']
		repo = e['repo']['name']
		forkee = e['payload']['forkee']['full_name']
		return user + ' forked the repo ' + repo + ' to ' + forkee
	
	def IssueCommentEvent(self, e):
		user = e['actor']['login']
		name = e['payload']['issue']['title'][:20]
		repo = e['repo']['name']
		url = self.shorten_url(e['payload']['issue']['html_url'])
		return user + ' commented on the issue ' + name + ' at ' + repo + ' - ' + url
	
	def WatchEvent(self, e):
		user = e['actor']['login']
		repo = e['repo']['name']
		return user + ' starred ' + repo + '.'
	
	def CreateEvent(self, e):
		user = e['actor']['login']
		reft = e['payload']['ref_type']
		repo = e['repo']['name']
		url = self.shorten_url(e['payload']['repository']['html_url'])
		return user + ' created a ' + reft + ' at ' + repo + ' - ' + url
	
	def PullRequestEvent(self, e):
		user = e['actor']['login']
		action = e['payload']['action']
		repo = e['repo']['name']
		url = self.shorten_url(e['payload']['pull_request']['html_url'])
		return user + ' ' + action + ' a pull request to ' + repo + ' - ' + url

if __name__ == '__main__':
	while True:
		gitbot = AutoGitBot('irc.freenode.net', 6667)
		time.sleep(10)
