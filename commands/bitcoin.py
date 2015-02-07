import urllib.request
import json
metaData = {"help": ["This command will show bitcoin prices.","Useage: &botcmdbitcoin"], "aliases": ["btc", "bit", "bitcoin"], "owner": 0 }

def urlDownload( url ):
		try:
			response 	= urllib.request.urlopen(url) 
		except UnicodeEncodeError:
			return "Aww maaaaaan. I ran into some jank characters there. Decode error, sorry :P"
		except:
			return 0

		return response.read().decode('utf-8')


def execute(command, user, host, channel, params ):
	if len( params ) > 0:
		btype 	= params[0]
	else:
		btype 	= "USD"

	htmlData 	= urlDownload("http://api.bitcoincharts.com/v1/weighted_prices.json")
	bitData 	= json.loads( htmlData )

	if not any( btype == bittype for bittype in bitData ):
		btype 	= "USD"
	
	price 		= bitData[btype]["24h"]
	return "The current price of the bitcoin is " + str( price ) + " " + btype + "'s."
