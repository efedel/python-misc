#!/usr/bin/python

import threading
import time

class TaskQueueProcessor(threading.Thread):
	'''
		General processor for the queue. Removes an item and
		handles it. Intended to run in its own thread.
	'''
	def __init__( self, name, queue ):
		''' queue is a TaskQueue object '''
		threading.Thread.__init__(self, None, None, name)
		self._queue = queue
		self._name = name

	def run(self):
		self._cont = True

		while ( self._cont ):
			# inner loop forces all queue items to
			# be read before queue fully shuts down
			while self._queue.count():
				t = self._queue.get()
				if t is not None:
					t.run()
				# allow other things to run
				time.sleep(1)
			# nothing to read ... sleep a bit
			time.sleep(1)
		return

	def stop(self):
		# this is the only place _cont is written after __init__
		self._cont = False

class TaskQueue(object):
	''' General Task Queue object. 
	    Can be subclassed to have a DB-backed queue, 
	    a priority queue, etc
	'''
	TASK_IMMEDIATE=0	# perform before normal tasks
	TASK_NORMAL=1
	TASK_DEFERRED=2		# perform after normal tasks
	TASK_LATE=3		# perform after deferred tasks
	TASK_IDLE=4		# perform only when system is idle

	def __init__(self, num_threads):
		self._pool = []
		self._tasks = ( [], [], [], [], [] )
		self._task_lock = threading.Lock()

		# different lists for each task type?
		for i in range(1, num_threads+1):
			t = TaskQueueProcessor('TaskQueueProc' + str(i), self)
			self._pool.append( t )
			t.start()

	def shutdown(self):
		for t in self._pool:
			t.stop()
			t.join()
		# TODO: save queue?
		

	def add(self, task, priority=1):
		''' add a task from the tail of the queue '''
		''' task is a callable '''

		self._task_lock.acquire()

		if priority is None:
			priority = 1
		elif priority < 0:
			priority = 0
		elif priority > 4:
			priority = 4

		self._tasks[priority].append(task)

		self._task_lock.release()

		return True

	def get(self):
		''' remove a task from the head of the queue '''

		item = None

		self._task_lock.acquire()

		for q in self._tasks:
			if len(q):
				# remove last item in queue
				item = q[0]
				del q[0]
				break

		self._task_lock.release()
		return item

	def peep(self):
		''' return a copy of the task at the head of the queue,
		    without locking the queue
		'''
		item = None

		for q in self._tasks:
			if len(q):
				# copy last item in queue
				item = q[0]
				break
		return item
	
	def count(self):
		''' return number of tasks in queue '''
		''' this allows things like:
			main():
				q = TaskQueue(1)
				# a processing thred is running
				q.add( task )
				...
				while q.count():
					t = q.get
					t()
		'''

		self._task_lock.acquire()

		count = len(self._tasks[0]) + len(self._tasks[1]) + \
		        len(self._tasks[2]) + len(self._tasks[3]) + \
		        len(self._tasks[4])

		self._task_lock.release()

		return count

