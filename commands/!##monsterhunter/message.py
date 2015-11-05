import json

meta_data	= { 'help': ['Saves a message to be sent to a user when they join a channel next.', 'Usage: &botcmdmessage <user> <message>'], 'aliases': ['message', 'pounce', 'msg'], 'owner': 0 }

def execute(parent, commands, user, host, channel, params):
	if len(params) < 2:
		return [meta_data['help'][1]]
	
	with open(parent.def_dir + '/commands/messages','r') as mfile:
		message_data = mfile.read()
	
	try:
		messages = json.loads(message_data)
	except ValueError:
		messages = {}
	
	sender = user
	reciever = params[0].lower()
	message = ' '.join(params[1:])
	
	if reciever in ['nickserv', 'chanserv', 'nickserv']:
		return ['I have been told to not send messages to them.']

	if reciever not in messages:
		messages[reciever] = {}
	
	if sender in messages[reciever]:
		messages[reciever][sender].append(message)
	else:
		messages[reciever][sender] = [message]
	
	with open(parent.def_dir + '/commands/messages', 'w') as mfile:
		mfile.write(json.dumps(messages))
	return ['The message will be passed on to {}.'.format(reciever)]
