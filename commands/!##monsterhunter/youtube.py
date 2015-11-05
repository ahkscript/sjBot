#!/usr/bin/env python3


import urllib.request
import json


meta_data = {'help': ['Searches youtube for a video.'], 'aliases': ['youtube', 'yout', 'ytb'], 'owner': 0}

def execute(parent, commands, user, host, channel, params):
	search = '%20'.join(params)
	data = parent.download_url('https://www.googleapis.com/youtube/v3/search?key=' + parent.keys['google'] + '&part=id,snippet&q=' + search)
	results = json.loads(data)
	if 'videoId' not in results['items'][0]['id']:
		return 'Could not find info for that video.'
	return '\x02' + results['items'][0]['snippet']['title'] + '\x02 - https://www.youtube.com/watch?v=' + results['items'][0]['id']['videoId']