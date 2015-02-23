import bot
import json
import urllib.request
import os
import re

formats = {'PushEvent': '{actor[login]} pushed {payload[size]} commit[s] to {repo[name]} - https://github.com/{repo[name]}/commits/master',
		'IssuesEvent': '{actor[login]} {payload[action]} the issue at {repo[name]} - {payload[issue][html_url]}',
		'ForkEvent': '{actor[login] forked the repo {repo[name]} to {payload[forkee][full_name]}.',
		'IssueCommentEvent': '{actor[login]} commented on the issue {payload[issue][title]} at {repo[name]} - {payload[issue][html_url]}',
		'WatchEvent': '{actor[login]} starred {repo[name]}',
		'CreateEvent': '{actor[login]} created a {payload[ref_type]} at {repo[name]} - {payload[repository][html_url]}',
		'PullRequestEvent': '{actor[login]} {payload[action]} a pull request to {repo[name]} - {payload[pull_request][html_url]}'}

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
				if ev['type'] in formats:
					data = formats[ev['type']].format(**ev)
					match = re.search('https://.*github.com.*', data)
					if match is not None:
						data = data.replace(match.group(0), self.shorten_url(match.group(0)))
					self.irc.privmsg('#ahkscript', data)
					
			with open(self.def_dir + '/old_events', 'w') as wfile:
					wfile.write(json.dumps(new_data))
		return 0

if __name__ == '__main__':
	gitbot = AutoGitBot('irc.freenode.net', 6667)
