import urllib.request
import json
meta_data = {"help": ["This command will show bitcoin prices.","Usage: &botcmdbitcoin"], "aliases": ["btc", "bit", "bitcoin"], "owner": 0 }


def execute(parent, commands, user, host, channel, params ):
	if len( params ) > 0:
		btype 	= params[0]
	else:
		btype 	= "USD"

	htmlData 	= parent.download_url("http://api.bitcoincharts.com/v1/weighted_prices.json")
	bitData 	= json.loads( htmlData )

	if not any( btype == bittype for bittype in bitData ):
		btype 	= "USD"
	
	price 		= bitData[btype]["24h"]
	return ['The current price of the bitcoin is ' + str( price ) + ' ' + btype + '.']
