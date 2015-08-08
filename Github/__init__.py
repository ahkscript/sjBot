#!/usr/bin/env python3


import urllib.request
import json
import Github.Repos
import Github.Gists
import Github.Commits
import Github.Reference
import Github.Blobs
import Github.Trees
import Github.Issues
import Github.Search
import Github.Users
import Github.Release


token = None
base_url = 'https://api.github.com/'


def api(url, headers={}, data=None, method=None):
	if data:
		if isinstance(data, list):
			data = bytes(json.dumps(data), 'utf-8')
		else:
			params = {}
			for item in data:
				if data[item] is not None:
					params[item] = data[item]
			data = bytes(json.dumps(params), 'utf-8')
		request = urllib.request.Request(url, data=data, headers=headers)
	else:
		request = urllib.request.Request(url, headers=headers)

	if method is not None:
		request.method = method
	return urllib.request.urlopen(request)


def decode(response):
	return json.loads(response.read().decode('utf-8'))


def commit_to_master(user, repo, files, commit_message, overwrite=False,
				   name=None, email=None, date=None):
	ref = Github.Reference.get_reference(user, repo)
	base_commit = Github.Commits.get_commit(user, repo, ref['object']['sha'])
	if overwrite is False:
		base_tree = base_commit['tree']['sha']
	else:
		base_tree = None
	tree = Github.Trees.create_tree(user, repo, files, base_tree)
	new_commit = Github.Commits.create_commit(user, repo, commit_message,
											  tree['sha'],
											  [ref['object']['sha']],
											  name, email, date)
	Github.Reference.update_reference(user, repo, sha=new_commit['sha'])
	return new_commit


def make_file(filename, content, mode='100644'):
	tree = {'path': filename, 'type': 'blob', 'mode': mode,
			'content': content}
	return tree