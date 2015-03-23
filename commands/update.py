import urllib.request
meta_data 	= {"help": ["This command give a link to the latest maintained versoin of AHK.", "Usage: &botcmdupdate"], "aliases": ["update", "u", "latest", "version"], "owner": 0 }


def execute(parent, commands, user, host, channel, params):
	version = parent.download_url('http://ahkscript.org/download/1.1/version.txt')
	return ["The latest AutoHotkey installer ( v" + version + " ) can be found at - " + parent.shorten_url('http://ahkscript.org/download/ahk-install.exe')]
