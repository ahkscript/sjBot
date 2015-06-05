#!/usr/bin/env python3


import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import time

meta_data = { "help": ["Starts the RSS."], "aliases": ["rss"], "owner": 1 }
rss_url = 'http://www.donationcoder.com/forum/index.php?action=.xml;type=rss2;limit=10'
channel = ['#donationcoder']


class htmlStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.data = []
		self.prepend = []
	
	def handle_data(self, data):
		self.data.append(data)
	
	def get_data(self):
		return ''.join(self.data)

def strip(html, item):
	if 'author' in item.tag:
		if len(item):
			return item[0].text
	s = htmlStripper()
	if html == None:
		return None
	s.feed(html)
	return s.get_data()


def strbrackets(data):
	if '}' in data:
		return data[data.find('}')+1:]
	return data


def rsstoobj(rss):
	output = []
	root = ET.fromstring(rss)
	items = root.findall('.//item')

	for child in items:
		output.append({strbrackets(i.tag):strip(i.text, i) for i in child})
	return output

def execute(parent, commands, user, host, channel, params):
	do_rss(parent)
	return 0


def do_rss(bot):
	first = 0
	while first == 0:
		first = rss_data = bot.download_url(rss_url)
	previous = rsstoobj(bot.html_decode(rss_data))
	while True:
		rss_data = bot.download_url(rss_url)
		if rss_data == 0:
			continue
		obj = rsstoobj(bot.html_decode(rss_data))
		if obj != previous:
			difference = [x for x in obj if x not in previous]
			for item in difference:
				title = item['title']
				url = item['link']
				author = item['aposter']
				category = item['category']

				for ch in channel:
					bot.privmsg(channel, author + ' - ' + category + ' - ' + 
						        title + ' - ' + bot.shorten_url(url))
			previous = obj
		time.sleep(60)