#!/usr/bin/env python3


import Github


def get_my_gists(since=None):
	data = {'since': since}
	response = Github.api(Github.base_url + 'gists',
						  {'Authorization': 'token ' + Github.token}, data)
	return Github.decode(response)


def get_gist(sha):
	response = Github.api(Github.base_url + 'gists/' + sha,
						  {'Authorization': 'token ' + Github.token},
						  method='GET')
	return Github.decode(response)


def get_user_gists(user, since=None):
	data = {'since': since}
	response = Github.api(Github.base_url + 'users/' + user + '/gists',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def create_gist(files, description, public=True):
	data = {'files': files, 'description': description, 'public': public}
	response = Github.api(Github.base_url + 'gists',
						  {'Authorization': 'token ' + Github.token}, data)
	return Github.decode(response)


def get_gist_commits(sha):
	response = Github.api(Github.base_url + 'gists/' + sha + '/commits',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def fork_gist(sha):
	response = Github.api(Github.base_url + 'gists/' + sha + '/forks',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def star_gist(sha):
	response = Github.api(Github.base_url + 'gists/' + sha + '/star',
						  {'Authorization': 'token ' + Github.token,
						  'Content-Length': 0}, method='PUT')
	return Github.decode(response)


def unstar_gist(sha):
	response = Github.api(Github.base_url + 'gists/' + sha + '/star',
						  {'Authorization': 'token ' + Github.token},
						  method='DELETE')
	return Github.decode(response)


def is_starred(sha):
	try:
		response = Github.api(Github.base_url + 'gists/' + '/star',
						  	  {'Authorization': 'token ' + Github.token},
						  	  method='GET')
	except utllib.error.HTTPError:
		return False
	if response.getcode() == 204:
		return True