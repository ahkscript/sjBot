import json
import os
meta_data	= { "help": ["Adds or removes a user to the notify list", "&botcmdmonitor <add/remove/list> <user>"], "aliases": ["monitor", "mon"], "owner": 0 }



def execute(parent, command, user, host, channel, params ):
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
			return {'Status': 0, 'Text': "Here is your monitor list: " + ', '.join( monData[ user ] ) + ".", 'Error': 'No Error'}
		except:
			return {'Status': 0, 'Text': "You don't have a list yet.", 'Error': 'No Error'}

	if params[0] == "add":
		for k in params[1:]:
			if len( monData[ user ] ) == 15:
				return {'Status': -1, 'Text': "You have reached your monitor limit", 'Error': 'Monitor Limit'}
			
			if k in monData[ user ]:
				continue

			monData[ user ].append( k )
			command[4].monitor( k )
		open('/'.join( os.path.dirname( os.path.realpath(__file__)).split("/")[:-1] ) + "/monlist", "w").write( str(monData).replace("'", '"') )
		return {'Status': 0, 'Text': "Users added to your list: " + ', '.join( params[1:] ) + ".", 'Error': 'No Error'}

	if params[0] == "remove":
		for k in params[1:]:
			monData[ user ].remove( k )
			command[4].stop_monitor( k )
		open('/'.join( os.path.dirname( os.path.realpath(__file__)).split("/")[:-1] ) + "/monlist", "w").write( str(monData).replace("'", '"') )
		return {'Status': 0, 'Text': "Users removed from your list: " + ', '.join( params[1:] ) + ".", 'Error': 'No Error'}

	return {'Status': -1, 'Text': "Please specify add, list or remove.", 'Error': 'Insufficient params'}
