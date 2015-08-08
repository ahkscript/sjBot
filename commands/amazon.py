import json
meta_data = {"help": ["This command will search amazon.","Usage: &botcmdamazon <query>"], "aliases": ['amazon','az'], "owner": 0 }

def execute(parent, commands, user, host, channel, params ):
	if len(params) == 0:
		return [meta_data['help'][1]]
	search = 'site:www.amazon.com%20' + '%20'.join(params)
	try:
		download = parent.download_url('https://www.googleapis.com/customsearch/v1?key=' + parent.keys['google'] + '&cx=009062493091172133168:4ckmchbpuzy&q=' + search)
	except UnicodeDecodeError:
		return ['No Data Found!']
	
	with open('commands/more.search', 'w') as more:
		more.write(download)

	response = json.loads(download)
	try:
		title = response['items'][0]['title']
		url = response['items'][0]['link']
	except IndexError:
		return 'No Data Found!'
	return ['\x02' + title + ' - \x02' + url]
