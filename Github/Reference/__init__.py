#!/usr/bin/env python3


import Github


def get_reference(user, repo, ref='heads/master'):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/refs/' + ref,
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def update_reference(user, repo, ref='heads/master', sha=None, force=False):
	data = {'sha': sha, 'force': force}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/refs/' + ref,
						  {'Authorization': 'token ' + Github.token}, data,
						  'PATCH')
	return Github.decode(response)