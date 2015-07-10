#!/usr/bin/env python3


import Github


def get_my_repos():
	response = Github.api(Github.base_url + 'user/repos',
				   {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def get_user_repos(user):
	response = Github.api(Github.base_url + user + 'repos',
				   {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def get_org_repos(org):
	response = Github.api(Github.base_url + 'orgs/' + org + '/repos',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def create_repo(name, description=None, homepage=None, auto_init=None,
			   private=False, gitignore_template=None, has_issues=True,
			   has_wiki=True, has_downloads=True, team_id=None,
			   license_template=None):
	data = {'name': name, 'description': description, 'homepage': homepage,
			'auto_init': auto_init, 'private': private,
			'gitignore_template': gitignore_template, 'has_issues': has_issues,
			'has_wiki': has_wiki, 'has_downloads': has_downloads,
			'team_id': team_id, 'license_template': license_template}
	response = Github.api(Github.base_url + 'user/repos',
						  {'Authorization': 'token ' + Github.token},
						  data=data)
	return Github.decode(response)


def get_information(user, repo):
	response = Github.api(Github.base_url + 'user/repos',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def get_contributors(user, repo, show_anon=None):
	data = {'anon': show_anon}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/contributors',
						  {'Authorization': 'token ' + Github.token}, data)
	return Github.api(response)


def get_language(user, repo):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo + 
						  '/languages',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def get_treams(user, repo):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/teams',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def get_tags(user, repo):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/tags',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)


def get_branches(user, repo):
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/branches',
						  {'Authorization': 'token ' + Github.token})
	return Github.decode(response)