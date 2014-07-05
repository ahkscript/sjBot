import urllib2
import urllib
import json
import sys

params 				= self.fullData

if len(params) < 0:
	output 			= "Weather needs more params"


url				= 'http://api.openweathermap.org/data/2.5/weather?q=' + self.paramData.replace(" ", "+") + "&units=metric"
hdr 			= {'User-Agent': 'Mozilla/5.0'} 
request 		= urllib2.Request( url, headers=hdr)
response 		= urllib2.urlopen( request)
html			= response.read()
output 			= json.loads( html)

weather 		= output["weather"][0]["description"]
		

windspeed 		= str( output["wind"]["speed"] ) + " km/h"

try:
	windgust 		= "a gust of " + str( output["wind"]["gust"] ) + " km/h"
except:
	windgust 		= "no gust"

winddirection 	= output["wind"]["deg"]
city 			= output["name"]

if winddirection > 45 and winddirection < 135:
	winddirection	= "westerly" 
if winddirection > 135 and winddirection < 225:
	winddirection 	= "northerly"
if winddirection > 225 and winddirection < 315:
	winddirection	= "easterly"
if winddirection > 315 and winddirection < 45:
	winddirection 	= "southerly"

if city 		== "":
	city 		= output["sys"]["country"]

temperature 		= output["main"]["temp"]
humidity		= str( output["main"]["humidity"] ) + "%"

output		= "The weather in " + city + " : " + weather + ", with a temperature of " + str( temperature ) + " c ( " + str( temperature*9/5+32  ) + " F ) and a humidity of " + humidity  + ". The wind is a " + str( winddirection ) + " at " + str( windspeed ) + " with " +  str( windgust )
