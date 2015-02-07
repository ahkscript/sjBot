import os

def is_online(this, params, online):
	with open(os.path.dirname(os.path.realpath(__file__)) + '/monitor_list', 'r') as myFile:
		data = myFile.read()
		monitor_list = json.loads( data )
	
	params = params.split(' ')
	if params[2] == this.botname:
		return 0

	user 		= params[3].split("!")[0][1:]
	for us in monitor_list:
		for cus in monitor_list[ us ]:
			if cus == user:
				this.irc.notice( us,  user + ' is online' if online else user + ' is offline')


def on376(this, params):
	with open(os.path.dirname(os.path.realpath(__file__)) + '/monitor_list', 'r') as myFile:
		data = myFile.read()
	monitor_list = json.loads( data )
	user_list = []
	for us in monitor_list:
		for user in monitor_list[us]: 
			if user in user_list:
				continue
			user_list.append(user)
		
	this.irc.monitor( user_list )
	return 0

def on730(this, params):
	is_online(this, params, 1)
	return 0

def on731(this, params):
	is_online(this, params, 0)
