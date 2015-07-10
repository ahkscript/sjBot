#!/usr/bin/env python3


import Github


def create_blob(user, repo, content, encoding='utf-8'):
	data = {'content': content, 'encoding': encoding}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/blobs',
						  {'Authorization': 'token ' + Github.token},
						  data, 'POST')
	return Github.decode(response)


def get_blob(user, repo, sha):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/blobs/' + sha,
						  {'Authorization': 'token ' + Github.token},
						  None, 'GET')
	return Github.decode(response)