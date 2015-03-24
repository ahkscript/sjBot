sjBot is a Python IRC Bot made by Sjc1000 ( Steven J. Core )
	Copyright © 2015, Steven J. Core

This file explains how to modify sjBot for your own use. It will also
explain how to make plugins or commands for sjBot. If you have any
questions don't hesitate to contact me:
	- Email: 42Echo6Alpha@gmail.com
	- IRC: irc.freenode.net, #Sjc_Bot
	
##First off, i will explain how to modify sjBot so he doesn't use my credentials.
You will find a sjbot.settings file in this directory, in there are things such as nickname, channels and bot trigger. You will NEED to change:
	- nickname
	- host
	- user
	- realname
	- channel_list
	- owner_list
	
Those are the things that you will HAVE to change. The others can stay as they are until you wish to change them.
	
###Ill explain what all the settings are and what they do:
	- network 	- The IRC network for the bot to join.
	- port 		- The port to join on. Usually 6667.
	- nickname 	- The nickname of the bot.
	- host 		- The host of the bot.
	- user 		- The bots username.
	- realname 	- The realname of the bot.
	- channel_list 	- The channel list for the bot to join.
	- botcmd 	- The trigger for the bots commands. Can be channel specific
	- default_cmd	- The default command to run if no command is found. Can be channel specific.
	- ignore 	- Characters at the start of a command to ignore.
	- owner_list 	- A list of owners hostmasks ( can be partial hostmask ) that can use owner commands.


##Commands:
Now that you're running your own bot you might want to make your own commands.
First off, you will need to create a .py file in the /commands folder. This is where sjBot finds all the commands.
Name it what you want your command to be. For example: google.py   will run when i use `google. You can add more things to the list that runs this file in the next step. YOU HAVE TO HAVE THE .py EXTENSION.

###meta_data:
You will need to add a meta_data dictionary to the top of your file ( below the imports ). sjBot will read this to find info about the command. They keys in this dictionary should be
	- help : A list containing help information, The first item being what it does, second being how its used.
	- aliases: A list of alternative commands that will call this file.
	- owner: A boolean value, 1 or 0. 1 if only the owner can use this file ( specified in owner list ) 0 if anyone can use it.

That is all the meta_data required, you can add more to this if you like but it will not be used by sjBot. In a command file you can use commands['commandname'].meta_data to get this info.

You also need to define a certain function for sjBot to run. This is called execute(). This function looks something like:

def execute(parent, commands, user, host, channel, params):
	* do stuff *
	return ['Text to send to channel']

###The params:
	- parent: 	The sjBot module. Where you can access everything from.
	- commands:	The commands sjBot has loaded. You will find all the commands in the /commands folder.
	- user:		The nickname of the user who called the command.
	- host:		The host of the person who called the command.
	- channel:	The channel where it was called from.
	- params:	The params passed to the command. For example  `command param1 param2 param3

You can then do stuff in this function and return some data. This data will be sent to the channel it was called from. If you wish to send to other channels use parent.privmsg('#channel', 'data') and return 0.

There you have it :) Commands are easy huh?


##plugins:
Now, plugins are very different than commands. First i will have to explain how sjBot handles the data from IRC.

sjBot recieves data from IRC that looks something like:

:Sjc1000!~Sjc1000@hostmask PRIVMSG #Sjc_Bot :Hello this is a message

That is a normal channel message. sjBot splits this data by spaces and calls the second item as a function. For example the previous data would call onPRIVMSG()
sjBot passes the data as params, but removing the function name itself from the data. The params would be.
onPRIVMSG(self, fullhost, channel, *message)  ( self is there because sjBot is a class )

I use *message because there is an un-defined length of data after the channel.
Now, i know you must be thinking. 'But im making a plugin, not messing with sjBot himself'.
sjBot calls plugins in almost exactly the same way.

If i wanted to handle a PRIVMSG in a plugin i would use def onPRIVMSG(this, fullhost, privmsg, channel, *message)
There are 2 different params:
	- this		- This is the sjBot class. Its basically the same as passing self.
	- privmsg 	- The bot does not remove the message type from the params, so this will contain whatever the function name is. I know its useless but i have not changed it.

Alright, now we have our function defined in sjBot. You might be wondering if you just return the data like you do with the commands. THIS IS NOT THE CASE.

plugins should not return data. However, this does not mean you can't send data to the channel.
Use this.privmsg('#channel', 'data')  to send data back to the channel.
You can also use this.send('ANY KIND OF IRC INFO')   send does not require the trailing \r\n it is handled in there.
this.send('JOIN #Sjc_Bot')  would make sjBot join the #Sjc_Bot channel.

Done! You can now make plugins for sjBot!
