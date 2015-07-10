#!/usr/bin/env python3


import Github


def repositories(query, sort=None, order='desc'):
	data = {'q': query, 'sort': sort, 'order': order}
	resposne = Github.api(Github.base_url + 'search/repositories',
						  {'Authorization': 'token ' + Github.token}, data,
						  'GET')
	return Github.decode(response)


def code(query, sort=None, order='desc'):
	data = {'q': query, 'sort': sort, 'order': order}
	response = Github.api(Github.base_url + 'search/code',
						  {'Authorization': 'token ' + Github.token}, data,
						  'GET')
	return Github.decode(response)


def issues(query, sort=None, order='desc'):
	data = {'q': query, 'sort': sort, 'order': order}
	response = Github.api(Github.base_url + 'search/issues',
						  {'Authorization': 'token ' + Github.token}, data,
						  'GET')
	return Github.decode(response)


def users(query, sort=None, order='desc'):
	data = {'q': query, 'sort': sort, 'order': order}
	response = Github.api(Github.base_url + 'search/users',
						  {'Authorization': 'token ' + Github.token}, data,
						  'GET')
	return Github.decode(response)