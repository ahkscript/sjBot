import json


def check_message(this, user):
	try:
		with open(this.def_dir + '/commands/messages', 'r') as mfile:
			message_data = json.loads(mfile.read())
	except FileNotFoundError:
		message_data = {}
	except ValueError:
		message_data = {}
	
	loop_data = message_data
	if user in loop_data:
		messages = loop_data[user]
		remove = []
		for sender in messages:
			sent_messages = messages[sender]
			ammount = str(len(sent_messages))
			this.privmsg(user, '{} has sent you {} message[s]:'.format(sender, ammount))
			
			for message in sent_messages:
				this.privmsg(user, message)
			
			remove.append(sender)
		
		for send in remove:
			del message_data[user][send]
		
		if message_data[user] == {}:
			del message_data[user]
	
	with open(this.def_dir + '/commands/messages', 'w') as mfile:
		mfile.write(json.dumps(message_data))
	return 0

def onPRIVMSG(this, full_host, privmsg, channel, *message):
	user = full_host.split('!')[0][1:]
	check_message(this, user)

def onJOIN(this, full_host, join, channel):
	user = full_host.split('!')[0][1:]
	check_message(this, user)
