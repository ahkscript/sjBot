import json


def check_message(this, user):
	try:
		with open(this.def_dir + '/commands/messages', 'r') as mfile:
			message_data = json.loads(mfile.read())
	except FileNotFoundError:
		message_data = json.dumps({})
	
	loop_data = message_data
	if user in loop_data:
		messages = message_data[user]
		for sender in messages:
			sent_messages = messages[sender]
			ammount = str(len(sent_messages))
			this.irc.privmsg(user, '{} has sent you {} message[s]:'.format(sender, ammount))
			
			for message in sent_messages:
				this.irc.privmsg(user, message)
			
			remove = sender
		del message_data[user][remove]
	
	with open(this.def_dir + '/commands/messages', 'w') as mfile:
		mfile.write(json.dumps(message_data))
	return 0

def onPRIVMSG(this, full_host, privmsg, channel, *message):
	user = full_host.split('!')[0][1:]
	check_message(this, user)

def onJOIN(this, full_host, join, channel):
	user = full_host.split('!')[0][1:]
	check_message(this, user)
