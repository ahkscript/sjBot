#!/usr/bin/env python3


import Github


def create_commit(user, repo, message, tree, parents=None, name=None,
				 email=None, date=None):
	data = {'message': message, 'tree': tree, 'parents': parents}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/commits',
						  {'Authorization': 'token ' + Github.token},
						  data, 'POST')
	return Github.decode(response)


def get_commits(user, repo, sha=None, path=None, author=None, since=None,
			   until=None):
	data = {'sha': sha, 'path': path, 'author': author, 'since': since,
			'until': until}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/commits',
						  {'Authorization': 'token ' + Github.token}, data,
						  'GET')
	return Github.decode(response)


def get_commit(user, repo, sha):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/commits/' + sha,
						  {'Authorization': 'token ' + Github.token},
						  method='GET')
	return Github.decode(response)