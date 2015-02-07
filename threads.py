from queue import Queue
from threading import Thread
import threading

class thread():
	def __init__(self, workers=4, queue_size=0):
		self.queue = Queue(queue_size)
		self.make_workers(workers)
		self.workers = threading.active_count() - 1
	
	def worker(self):
		while True:
			task = self.queue.get()
			try:
				function = getattr(task['module'], task['function'])
			except AttributeError:
				continue
			
			if task['params'] == ['']:
				function()
			else:
				function(*task['params'])
			self.queue.task_done()
		return -1

	def add_task(self, command, params, module=__name__, join=0):
		if threading.active_count() - 1 < self.workers:
			self.make_workers(self.workers - threading.active_count() - 1)

		if isinstance(params, str):
			params = [ params ]
		self.queue.put({'function': command, 'module': module, 'params': params})
		if join:
			self.queue.join()
		return 0

	def make_workers(self, workers):
		for i in range(workers):
			thread = Thread(target=self.worker)
			thread.daemon = True
			thread.start()
		return 0
