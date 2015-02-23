import json
import os
meta_data	= { "help": ["Adds or removes a user to the notify list", "&botcmdmonitor <add/remove/list> <user>"], "aliases": ["monitor", "mon"], "owner": 0 }



def execute(parent, commands, irc, user, host, channel, params):
	try:
		data 		= open( '/'.join( os.path.dirname( os.path.realpath(__file__)).split("/")[:-1] ) + "/plugins/monitor_list" ).read()
		monData 	= json.loads( data )
	except ValueError:
		monData 	= {}

	try:
		monData[ user ]
	except KeyError:
		monData[ user ] = []
	
	if params[0] == "list":
		try:
			return ["Here is your monitor list: " + ', '.join( monData[ user ] ) + "."]
		except:
			return ["You don't have a list yet."]

	if params[0] == "add":
		for k in params[1:]:
			if len( monData[ user ] ) == 15:
				return ["You have reached your monitor limit"]
			
			if k in monData[ user ]:
				continue

			monData[ user ].append( k )
			command[4].monitor( k )
		open('/'.join( os.path.dirname( os.path.realpath(__file__)).split("/")[:-1] ) + "/monlist", "w").write( str(monData).replace("'", '"') )
		return ["Users added to your list: " + ', '.join( params[1:] ) + "."]

	if params[0] == "remove":
		for k in params[1:]:
			monData[ user ].remove( k )
			command[4].stop_monitor( k )
		open('/'.join( os.path.dirname( os.path.realpath(__file__)).split("/")[:-1] ) + "/monlist", "w").write( str(monData).replace("'", '"') )
		return ["Users removed from your list: " + ', '.join( params[1:] ) + "."]

	return ["Please specify add, list or remove."]
