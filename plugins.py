import imp
from os import listdir

class plugin():
	def __init__(self, folder):
		self.folder = folder
		self.load_plugins()
	
	def load_plugins(self):
		files = listdir(self.folder)
		self.plugins = {}
		for f in files:
			if '.py' in f:
				current = imp.load_source(f[:-3] + '_plug', self.folder + f )
				self.plugins[f[:-3]] = current

		return 0

	def load_metadata(self, command ):
		try:
			data = self.plugins[command].metaData
			self.metaData = data
		except AttributeError:
			return -1
		return data

	def run(self, command, params):
		try:
			function = getattr(self.plugins[command], 'execute')
		except AttributeError:
			return -1
		except KeyError:
			return -2
		return function(*params)

	def run_plugin(self, plugin, command, params):
		try:
			function = getattr(self.plugins[plugin], command )
		except AttributeError:
			return -1
		except KeyError:
			return -2
		return function(*params)
