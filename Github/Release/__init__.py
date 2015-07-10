#!/usr/bin/env python3


import Github


def create_release(user, repo, tag_name, target_sha, name, body, draft=False,
				  prerelease=False):
	data = {'tag_name': tag_name, 'target_commitsh': target_sha, 'name': name,
			'body': body, 'draft': draft, 'prerelease': prerelease}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/releases',
						  {'Authorization': 'token ' + Github.token}, data,
						  'POST')
	return Github.decode(response)