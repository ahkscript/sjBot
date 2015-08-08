#!/usr/bin/env python3


import Github


def get_issues(filter='assigned', state='open', labesl=None, sort=None,
			  direction='desc', since=None):
	data = {'filter': filter, 'state': state, 'labels': labels, 'sort': sort,
			'direction': direction, 'since': since}
	response = Github.api(Github.base_url + 'issues',
						  {'Authorization': 'token ' + self.token}, data,
						  'GET')
	return Github.decode(response)


def get_repo_issues(user, repo, milestone='*', state='open', assignee='*',
				  creator=None, mentioned=None, labels=None, sort='created',
				  direction='desc', since=None):
	data = {'milestone': milestone, 'state': state, 'assignee': assignee,
			'creator': creator, 'mentioned': mentioned, 'labels': labels,
			'sort': sort, 'direction': direction, 'since': since}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
					      '/issues',
					      {'Authorization': 'token ' + self.token}, data,
					      'GET')
	return Github.decode(response)


def create_issues(user, repo, title, body, assignee=None, milestone=None,
				labels=None):
	data = {'title': title, 'body': body, 'assignee': assignee,
	        'milestone': milestone, 'labels': labels}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/issues',
						  {'Authorization': 'token ' + self.token},
						  data, 'POST')
	return Github.api(response)


def edit_issues(user, repo, issue_number, title, body, assignee=None,
			  state='open', milestone=None, labels=None):
	data = {'title': title, 'body': body, 'assignee': assignee,
			'state': state, 'milestone': milestone, 'labels': labels}
	response = Github.api(Github.base_url + 'repos/' + user + '/' + repo +
						  '/issues/' + str(issue_number),
						  {'Authorization': 'token ' + self.token},
						  data, 'PATCH')
	return Github.api(response)