#!/usr/bin/env python3


import Github


def create_tree(user, repo, tree_array, base_tree=None):
	data = {'tree': tree_array, 'base_tree': base_tree}
	response = Github.api(Github.base_url + 'repos/' + user +'/' + repo +
						  '/git/trees',
						  {'Authorization': 'token ' + Github.token},
						  data, 'POST')
	return Github.decode(response)


def get_tree(user, repo, sha):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/git/trees/' + sha,
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)