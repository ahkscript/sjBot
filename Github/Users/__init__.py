#!/usr/bin/env python3


import Github


def get_user(username):
	response = Github.api(Github.base_url + 'users/' + username,
						  {'Authorization': 'token ' + Github.token},
						  method='GET')
	return Github.decode(response)


def get_authed_user():
	response = Github.api(Github.base_url + 'user',
						  {'Authorization': 'token ' + Github.token},
						  method='GET')
	return Github.decode(response)


def update_user(name, email=None, blog=None, company=None, location=None,
			   hireable=None, bio=None):
	data = {'name': name, 'email': email, 'blog': blog, 'company': company,
			'location': location, 'hireable': hireable, 'bio': bio}
	response = Github.api(Github.base_url + 'user',
						  {'Authorization': 'token ' + Github.token}, data,
						  'PATCH')
	return Github.decode(response)


def get_emails():
	response = Github.api(Github.base_url + 'user/emails',
						  {'Authorization': 'token ' + Github.token},
						  method='GET')
	return Github.decode(response)


def add_emails(*email):
	data = [x for x in email]
	response = Github.api(Github.base_url + 'user/emails',
						  {'Authorization': 'token ' + Github.token},
						  data, 'POST')
	return Github.decode(response)

def delete_emails(*email):
	data = [x for x in email]
	response = Github.api(Github.base_url + 'user/emails',
						  {'Authorization': 'token ' + Github.token},
						  data, 'DELETE')
	return response.getcode()