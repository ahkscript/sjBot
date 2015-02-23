import urllib.request
import json
import math

meta_data 	= { "help": ["Returns the weather for a specified city.","Usage: &botcmdweather <city>"], "aliases": ["weather", "we"], "owner": 0 }

def urlDownload( url ):
	try:
		response 	= urllib.request.urlopen(url) 
	except UnicodeEncodeError:
		return "Aww maaaaaan. I ran into some jank characters there. Encode error, bro :P"
	except:
		return "__notext__"

	return response.read().decode('utf-8')


def execute(parent, commands, irc, user, host, channel, params):
	if '&' in params:
		search = ' '.join( params ).split('&')[0]
	else:
		search = params

	weatherd = urlDownload('http://api.openweathermap.org/data/2.5/weather?q=' + '%20'.join(search) + '&units=metric')
	wObject = json.loads(weatherd)
	
	weather = {'city': {'name': wObject['name'], "coords": {'lon': wObject['coord']['lon'], 'lat': wObject['coord']['lat']}}, 'description': wObject['weather'][0]['description'], 'temp': {'current': {'celsius': wObject['main']['temp'], 'fahrenheit': math.ceil(( wObject['main']['temp'] * 9 ) / 5 + 32)}, 'min': {'celsius': wObject['main']['temp_min'], 'fahrenheit': math.ceil(( wObject['main']['temp_min'] * 9 ) / 5 + 32)}, 'max': {'celsius': wObject['main']['temp_max'], 'fahrenheit': math.ceil(( wObject['main']['temp_max'] * 9 ) / 5 + 32)}}, 'pressure': wObject['main']['pressure'], 'humidity': wObject['main']['humidity'], 'wind': {'speed': wObject['wind']['speed'], 'direction': wObject['wind']['deg'] }}

	if '&' in params:
		output = ''.join( ' '.join( params ).split('&')[1] ).format( **weather )
	else:
		output = 'The weather for {city[name]} is {description} with a temperature of {temp[current][celsius]}C ({temp[current][fahrenheit]}F).'.format( **weather)
	return [output]
