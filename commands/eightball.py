import random
metaData 	= { "help": ["Answers a question with a eightball response.","Usage: &botcmdeightball <question>"], "aliases": ["random", "eight", "eightball", "8ball"], "owner": 0 }

def execute(command, user, host, channel, params ):
	responses 	= ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definately.", "You may rely on it.", "As i see it, Yes.", "Most likely.", "Outlook good", "YUUSS!", "Signs point to yes.", "Reply is hazy, Try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
	return random.choice( responses )
