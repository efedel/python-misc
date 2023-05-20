#!/usr/bin/python

	
class BGLog(object):

	LOG_VERBOSE=0	# Useless messages
	LOG_DEBUG=1	# Debug messages
	LOG_TASK=2	# Notification of task init/completion
	LOG_NOTICE=3	# Notification of normal events
	LOG_WARN=4	# Warnings: errors that can be ignored
	LOG_ERROR=5	# Errors: warnings that should not be ignored
	LOG_CRIT=6	# Critical Errors: the system is down 
	LOG_ALL = (0, 1, 2, 3, 4, 5, 6)	# Everything
	LOG_ERR = (4,5,6)		# Only warnings and errors
	LOG_EVENT= (2,3)		# Only events

	_log_str = ( 'Verbose', 'Debug', 'Task', 'Notice', 'Warning',
	             'Error', 'Critical' )

	def __init__(self):
		self._subscribers = ( [], [], [], [], [], [], [] )

	def _validate_log_param(self, log):
		if log is None:
			return (,)
		if isinstance(log, list):
			return log
		if log < self.LOG_VERBOSE:
			log = self.LOG_VERBOSE
		elif log > self.LOG_CRIT:
			log = self.LOG_CRIT
		return (log,)

	def subscribe(self, subscriber, log):
		log = self._validate_log_param(log)
		for i in log:
			if subscriber not in self._subscribers[i]:
				i.append(subscriber)
	
	def unsibscribe(self, subscriber, log):
		if log = None:
			log = self.LOG_ALL
		log = self._validate_log_param(log)
		for i in log:
			if subscriber in self._subscribers[i]:
				# TODO
				pass

	def log(self, log, message):
		log = self._validate_log_param(log)
		for i in log:
			for s in self._subscribers[i]:
				s.(self._log_str[i], message)

# BGService Singleton: used by all objects in all threads to communicate
# with the service, and from there to the application
