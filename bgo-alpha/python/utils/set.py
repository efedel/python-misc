#!/usr/bin/python
'''
	Finite and Infinite Set Implementation

	x in S : 0 <= x <= 1.0
	(x, y) in S : 0 < x < y
'''

class Set(object):
	def __init__(self, data=None, expr=None, get_key=None, exclude=None):
		'''
		data : a list, tuple, dictionary, or a function
		       that returns one of the first three; the
		       values will be explicitly included in the
		       set. for use with finite or infinite sets.
		expr: lambda describing set membership conditions.
		      for use with infinite sets.
		get_key : should return an object that can be used
		          as a dictionary key 
		data : a list, tuple, dictionary, or a function
		       that returns one of the first three; the
		       values will be explicitly excluded from the
		       set. for use with infinite sets.
		'''

		self.__supersets = []
		self.__get_key = get_key
		self.__lambda = expr

		if self.__get_key == None:
			self.__get_key = self.__builtin_get_key

		# import data from first arg
		if callable(data):
			func = data
			data = func()

		if isinstance(data, tuple) or isinstance(data, list):
			# build dict from list/tuple
			self.__include = {}
			for i in data:
				self.__include[self.__get_key(i)] = i
		elif isinstance(data, dict):
			# copy dict
			self.__include = data.copy()
		else:
			# use empty dict
			self.__include = {}

		# import data from exclude arg
		if callable(exclude):
			func = exclude
			exclude = func()

		if isinstance(exclude, tuple) or isinstance(exclude, list):
			# build dict from list/tuple
			self.__exclude = {}
			for i in exclude:
				self.__exclude[self.__get_key(i)] = i
		elif isinstance(exclude, dict):
			# copy dict
			self.__exclude = exclude.copy()
		else:
			# use empty dict
			self.__exclude = {}

	def __builtin_get_key(self, obj):
		'''
		Return the provided parameter. This is an 
		internal version of 'get_key' which assumes 
		the object is a value.
		'''

		try:
			# use the object's hash if possible
			key = hash(obj)
		except TypeError:
			# else use the object's string representation
			key = str(obj)

		return key
			

	def contains(self, obj):
		'''
		Determines whether 'obj' is a member of the set
		This performs the following checks:
			* is the object explicitly excluded from the set?
			* is the object explicitly included in the set?
			* does the object pass the set's lambda?
		'''
		key = self.__get_key(obj)
		if key in self.__exclude:
			return False
		if key in self.__include:
			return True
		if self.__lambda is not None:
			return self.__lambda(obj)
		return False

	def subset(self, func=None):
		'''
		Generate a proper subset of this set. All additions to
		the subset will be reflected in this set. If func
		is specified, it is applied to each member in self;
		only members for which func returns True will be included
		in the output set. Returns the Empty set if the output
		set has no elements.
		'''
		S = Set(get_key=self.__get_key)
		S.__supersets.append(self)
		S.__lambda = self.__lambda

		if self.count() == 0:
			# an unfilled set is different from
			# the empty set -- it is 'initialized'
			return S

		for i in self.__exclude:
			S.__exclude[i] = self.__exclude[i]

		for i in self.__include:
			if func is None or func(self.__include[i]):
				S.add(self.__include[i])

		if S.__lambda is None and S.count() == 0:
			return EmptySet

		return S

	def superset(self):
		'''
		Return the superset of this set, if it is a proper subset
		'''
		if len(self.__supersets):
			return self.__supersets[0]
		return None

	def is_proper_subset(self, set):
		'''
		return true if set was generated from self, or one of
		its subsets, via the subset() method
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		for superset in set.__supersets:
			# if set.supersets contains id of self...
			if id(superset) == id(self):
				return True
			# else recurse on set.supersets.supersets
			elif self.is_proper_subset(superset):
				return True
		return False

	def is_proper_superset(self, set):
		'''
		return true if self was generated from set, or one of
		its supersets, via the subset() method
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		for superset in self.__supersets:
			# if self.supersets contains id of set...
			if id(superset) == id(set):
				return True
			# else recurse on self.supersets.supersets
			elif superset.is_proper_superset(set):
				return True
		return False

	def issubset(self, set):
		'''
		Determine if all elements in 'set' are in this set
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		if self.is_proper_subset(set):
			return True

		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, "Cannot compare infinite sets"

		# if all items in set are in self, return true
		for i in set.__include:
			if i not in self.__include or \
			   set.__include[i] != self.__include[i]:
				return False

		# if set has the same cardinality as self, return false
		if set.count() == self.count(): 
			return False

		return True

	def issubset_or_equiv(self, set):
		'''
		Determine if all elements in 'set' are in this set
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		if self.is_proper_subset(set):
			return True

		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, \
				"Cannot compare infinite sets"

		# if all items in set are in self, return true
		for i in set.__include:
			if i not in self.__include:
				return False

		return True

	def issuperset(self, set):
		'''
		Determine if all elements in this set are in 'set'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		if self.is_proper_superset(set):
			return True
			
		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, \
				"Cannot compare infinite sets"

		# if all items in self are in set, return true
		for i in self.__include:
			if i not in set.__include:
				return False

		# if set has the same cardinality as self, return false
		if set.count() == self.count(): 
			return False

		return True

	def issuperset_or_equiv(self, set):
		'''
		Determine if all elements in this set are in 'set'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		if self.is_proper_superset(set):
			return True

		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, \
				"Cannot compare infinite sets"

		# if all items in self are in set, return true
		for i in self.__include:
			if i not in set.__include:
				return False


		return True

	def equivalent(self, set):
		'''
		Determine if sets have a one-to-one correspondence
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, \
				"Cannot compare infinite sets"
			
		for i in self.__include:
			if i not in set.__include:
				return False

		if set.count() == self.count(): 
			return True

		return False


	def disjoint(self, set):
		'''
			returns true if S and S' have no elements in
			common
		'''
		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, \
				"Cannot compare infinite sets"

		for i in self.__include:
			# if in set, or if passes set's lambda and is not
			# excluded from set...
			if i in set.__include or (set.__lambda is not None and
			   set.__lambda(self.__include[i]) and
			   i not in set.__exclude):
				return False

		for i in set.__include:
			# if in self, or if passes self's lambda and is not
			# excluded from self...
			if i in self.__include or (self.__lambda is not None \
			   and self.__lambda(set.__include[i]) and
			   i not in self.__exclude):
				return False

		return True

	def union(self, set):
		'''
			returns the union or sum of S and S':
			all elements that are in either S or S'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		S = Set(get_key=self.__get_key)
		if self.__lambda is not None and set.__lambda is not None:
			S.__lambda = lambda x: self.__lambda(x) or \
				     set.__lambda(x)
		elif self.__lambda is not None:
			S.__lambda = self.__lambda
		elif set.__lambda is not None:
			S.__lambda = set.__lambda

		# copy all items in self
		S.__include = self.__include.copy()

		# copy any additional items from set
		for i in set.__include:
			if i not in self.__include:
				S.__include[i] = set.__include[i]

		# remove any conflicts in exclude lists
		for i in set.__exclude:
			if i not in S.__include:
				S.__exclude = set.__exclude[i]
		for i in self.__exclude:
			if i not in S.__include:
				S.__exclude = self.__exclude[i]

		if S.__lambda is None and S.count() == 0:
			return EmptySet

		# self and set are now proper subsets of the union set S
		self.__supersets.append(S)
		set.__supersets.append(S)

		return S

		
	def intersection(self, set):
		'''
			returns the intersection or product of S and S':
			all elements that are in both S and S'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		S = Set(get_key=self.__get_key)
		if self.__lambda is not None and set.__lambda is not None:
			S.__lambda = lambda x: self.__lambda(x) and \
				     set.__lambda(x)

		for i in self.__include:
			# if item is not excluded from set, and is included or 
			# passes set's lambda...
			if i not in set.__exclude and (i in set.__include or \
			    (set.__lambda is not None and 	\
			     set.__lambda(self.__include[i]) )):
				S.__include[i] = self.__include[i]

		for i in set.__include:
			# if item is not excluded from self and we have not
			# already processed it and it passes self's lambda...
			if i not in self.__exclude and		\
			   i not in self.__include and		\
			   self.__lambda is not None and 	\
			   self.__lambda(set.__include[i]) :
				S.__include[i] = set.__include[i]

		if S.__lambda is None and S.count() == 0:
			return EmptySet

		# neither self nor set is a proper superset of S

		return S

	def difference(self, set):
		'''
			returns the difference of S and S': all elements
			that are in S but not in S'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		S = Set(get_key=self.__get_key)
		if self.__lambda is not None and set.__lambda is not None:
			S.__lambda = lambda x: self.__lambda(x) and not \
				     set.__lambda(x)
		elif self.__lambda is not None:
			S.__lambda = self.__lambda

		for i in self.__include:
			# if not included in set, and is excluded from set
			# or set has no lambda or item fails set's lambda...
			if i not in set.__include and			\
			  (i in set.__exclude or set.__lambda is None or \
			   not set.__lambda(self.__include[i]) ):
				S.__include[i] = self.__include[i]

		for i in set.__include:
			# if i passes self's lambda...
			if self.__lambda is not None \
			   and self.__lambda(set.__include[i]) :
			   	# exclude from S: it is part of self
				S.__exclude[i] = set.__include[i]

		if S.__lambda is None and S.count() == 0:
			return EmptySet

		# S is now a proper subset of self (but not of set)
		S.__supersets.append(self)

		return S

	def symmetric_difference(self, set):
		'''
			returns all elements in S that are not in S',
			and all elements of S' that are not in S
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"
			
		S = Set(get_key=self.__get_key)
		if self.__lambda is not None and set.__lambda is not None:
			S.__lambda = lambda x : (self.__lambda(x) and not \
				     set.__lambda(x))  or 		\
				     (set.__lambda(x) and not 		\
				     self.__lambda(x))
		elif self.__lambda is not None:
			S.__lambda = self.__lambda
		elif set.__lambda is not None:
			S.__lambda = set.__lambda

		for i in self.__include:
			# if i included in set...
			if i in set.__include:
				continue

			# if i included in set or passes set's lambda...
			if set.__lambda is not None:
				# if i fails set's lambda, include it
				if not set.__lambda(self.__include[i]) :
					S.__include[i] = self.__include[i]
				# else exclude it explicitly
				else:
					S.__exclude[i] = self.__include[i]
			else:
				# fallthrough: add to S
				S.__include[i] = self.__include[i]

		for i in set.__include:
			# if i included in self...
			if i in self.__include:
				continue

			# if i included in self or passes set's lambda...
			if self.__lambda is not None:
				# if i fails self's lambda, include it
				if not self.__lambda(set.__include[i]) :
					S.__include[i] = set.__include[i]
				# else exclude it explicitly
				else:
					S.__exclude[i] = set.__include[i]
			else:
				# fallthrough: add to S
				S.__include[i] = set.__include[i]

		if S.__lambda is None and S.count() == 0:
			return EmptySet

		# neither self nor set is a proper superset of S

		return S

	def complement(self):
		'''
			returns the complement if S : theoretically,
			all elements of the universal set that are not
			in S.
		'''
		S = Set(get_key=self.__get_key)
		if self.__lambda is not None:
			S.__lambda = lambda x: not self.__lambda(x)
		S.__exclude = self.__include.copy()
		S.__include = self.__exclude.copy()

		if len(S.__include) == 0 and len(S.__exclude) == 0:
			return EmptySet

		# S has no proper superset

		return S

	def direct_product(self, set, func=None):
		'''
		Returns a set of tuples (x, y) of all x in S and all
		y in S'.
		'func' is a function that returns true or false for
		a given tuple (x, y); it can be used to limit the domain
		of the output set.
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"

		if self.__lambda is not None or set.__lambda is not None:
			raise AssertionError, "An infinite set cannot be mapped"
			
		S = Set()
		for i in self.__include:
			for j in set.__include:
				if func is None or func( (i, j) ):
					# add tuple to new set
					S.add( (i,j) )

		if S.count() == 0:
			return EmptySet

		# S has no proper superset

		return S

	# TODO:
	# is ... injection, surjection, bijection
	def power(self):
		'''
		Power Set : the set of all subsets of self
		'''
		if self.__lambda is not None:
			raise AssertionError, "An infinite set cannot be mapped"

		if len(self.__include) == 0:
			return EmptySet

		S = Set()
		keys = self.__include.keys()
		n = len(keys)
		for i in range(0,n):
			tmp = {}
			for j in range(i,n):
				tmp[keys[j]] = self.__include[keys[j]]
				S.add(Set(tmp))
		return S

	def map(self, map_func, get_key=None):
		'''
		foreach x in set S, apply 'map_func' to generate a new
		object x', and store x' in the new set S'
		Note that the map_func must meet the following criteria:
			+ it must generate a new object x' for storage in S'
			+ S'.get_key(x') must return the same value as 
			  S.get_key(x)
		'''
		if self.__lambda is not None:
			raise AssertionError, "An infinite set cannot be mapped"

		if len(self.__include) == 0:
			return EmptySet

		if get_key is None:
			func = self.__get_key
		else:
			func = get_key

		S = Set(get_key=func)

		for i in self.__include:
			obj = map_func(i)

			if get_key is not None:
				i = get_key(obj)

			S.__include[i] = obj

		if S.count() == 0:
			return EmptySet

		# S has no proper superset

		return S

	def update(self,set):
		'''
		replace this set with the union of this set and 'set'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"

		S = self.union(set)
		self.__include = S.__include.copy()
		self.__exclude = S.__exclude.copy()
		self.__lambda = S.__lambda
			
	def intersection_update(self, set):
		'''
		replace this set with the intersection of this set and 'set'
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"

		S = self.intersection(set)
		self.__include = S.__include.copy()
		self.__exclude = S.__exclude.copy()
		self.__lambda = S.__lambda
			
	def difference_update(self, set):
		'''
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"

		S = self.difference(set)
		self.__include = S.__include.copy()
		self.__exclude = S.__exclude.copy()
		self.__lambda = S.__lambda
			
	def symmetric_difference_update(self, set):
		'''
		'''
		if not isinstance(set, Set):
			raise AssertionError, "Argument is not a set"

		S = self.symmetric_difference(set)
		self.__include = S.__include.copy()
		self.__exclude = S.__exclude.copy()
		self.__lambda = S.__lambda
			

	def add(self, obj):
		'''
		add a new object to the set 
		Note: this adds the object to all proper supersets as well
		'''
		key = self.__get_key(obj)
		self.__setitem__(key, obj)

	def remove(self, obj):
		'''
		remove an object from the set
		Note: this has no effect on supersets
		'''
		key = self.__get_key(obj)
		self.__delitem__(key)

	def count(self):
		'''
		return the number of objects in the set
		'''
		if self.__lambda is not None:
			raise AssertionError, \
				"An infinite set cannot be counted"
		return len(self.__include)

	# ---------------- allow operators to be used ------------------
	def __add__(self, set):
		'''	+ : union			'''
		return self.union(set)
	
	def __mul__(self, set):
		'''	* : intersection		'''
		return self.intersection(set)

	def __sub__(self, set):
		'''	- : difference			'''
		return self.difference(set)
	
	def __or__(self, set):
		'''	| : union			'''
		return self.union(set)
	
	def __and__(self, set):
		'''	& : intersection		'''
		return self.intersection(set)

	def __xor__(self, set):
		'''	^ : symmetric difference	'''
		return self.symmetric_difference(set)

	def __eq__(self, set):
		'''	== : equivalence		'''
		return self.equivalent(set)

	def __ne__(self, set):
		'''	!= : not equivalent		'''
		return not self.equivalent(set)

	def __le__(self, set):
		'''	<= : subset or equivalent	'''
		return self.issuperset_or_equiv(set)

	def __lt__(self, set):
		'''	< : subset			'''
		return self.issuperset(set)

	def __ge__(self, set):
		'''	>= : superset or equivalent	'''
		return self.issubset_or_equiv(set)

	def __gt__(self, set):
		'''	> : superset			'''
		return self.issubset(set)

	def __iadd__(self, set):
		'''	+= : update/union		'''
		self.update(set)
		return self

	def __isub__(self, set):
		'''	-= : difference update		'''
		self.difference_update(set)
		return self

	def __imul__(self, set):
		'''	*= : intersection update	'''
		self.intersection_update(set)
		return self

	def __ior__(self, set):
		'''	|= update/union			'''
		self.update(set)
		return self

	def __iand__(self, set):
		'''	&= : intersection update	'''
		self.intersection_update(set)
		return self

	def __ixor__(self, set):
		'''	^= : symmetric difference update'''
		self.symmetric_difference_update(set)
		return self
	
	def __invert__(self):
		'''	~ : complement	'''
		return self.complement()

	# support container operations
	def __len__(self):
		'''	count of elements in set '''
		if self.__lambda is not None:
			raise AssertionError, \
				"An infinite set has no length"
			return
		return self.count()

	def __getitem__(self, key):
		''' return object for 'key' '''
		return self.__include[key] 

	def __setitem__(self, key, obj):
		''' insert/update item at 'key' '''
		self.__include[key] = obj
		if key in self.__exclude:
			del self.__exclude[key]
		# if this is a 'proper subset' then update superset
		for s in self.__supersets:
			s.add(obj)

	def __delitem__(self, key):
		''' remove item at 'key' '''
		if key not in self.__include:
			raise KeyError
		# explicitly exclude item if it passes self's lambda
		if self.__lambda is not None and \
		   self.__lambda(self.__include[key]):
			self.__exclude[key] = self.__include[key]
		del self.__include[key]

	def __contains__(self, object):
		''' is object in set? '''
		return self.contains(object)

	class SetIterator:
		def __init__(self, dict):
			self.__dict = dict
			self.__keys = dict.keys()

			# construct list of keys
			self.__keys.sort()
			self.__next = 0

		def __iter__(self):
			return self

		def next(self):
			if len(self.__keys) == 0 or self.__next == -1:
				raise StopIteration

			key = self.__keys[self.__next]
			self.__next = self.__next + 1
			if self.__next >= len(self.__dict):
				self.__next = -1
			return self.__dict[key]

	def __iter__(self):
		if self.__lambda is not None:
			raise AssertionError, \
				"An infinite set has no iterator"
		return Set.SetIterator(self.__include)

	def iterkeys(self):
		return self.__iter__()

	# misc object operators
	def __str__(self):
		return "{ " + str(self.__lambda) + " : " + 	\
		       str(self.__include) + 			\
		       " : " +  str(self.__exclude) + " }"

	def __nonzero__(self):
		''' All sets but the empty set are nonzero '''
		return True

	# --------------- aliases for method names --------------
	def card(self):
		''' cardinality: alias for count '''
		return self.count()

	def P(self):
		''' P() : alias for power set '''
		return self.power()

	def product(self, set):
		''' product() : alias for intersection '''
		return self.product(set)
		



class EmptySet(Set):
	'''
	The empty set (0). This has the following properties:
		+ it is a singleton
	'''
	def __call__(self):
		# make this a singleton by calling EmptySet = EmptySet()
		return self

	def contains(self, obj):
		'''
		The empty set 0 contains no elements
		'''
		return False

	def union(self, set):
		'''
		The union of the empty set 0 and a set S is S
		'''
		return set

	def intersection(self, set):
		'''
		The intersection of the empty set 0 and a set S
		is 0
		'''
		return self

	def difference(self, set):
		'''
		The difference of the empty set 0 and a set S
		is S
		'''
		return set

	def symmetric_difference(self, set):
		return set

	def direct_product(self, set):
		'''
		The direct product of the empty set 0 is 0
		'''
		return self
		
	def map(self, map_func, get_key=None):
		'''
		Attempting to map the empty set 0 returns 0
		'''
		return self

	def add(self, obj):
		pass

	def remove(self, obj):
		pass

	def update(self,set):
		pass

	def intersection_update(self, set):
		pass

	def difference_update(self, set):
		pass

	def symmetric_difference_update(self, set):
		pass

	def count(self):
		return 0

	def __nonzero__(self):
		return False

	def __iter__(self):
		return iter( () ) 

	def __getitem__(self, key):
		pass

	def __setitem__(self, key, obj):
		pass

	def __delitem__(self, key):
		pass

	def __str__(self):
		return "{ 0 }"

	def __len__(self):
		return 0


class UberSet(Set):
	'''
	The set of all sets and objects. This has the following properties:
		+ it is a singleton
	'''
	def __call__(self):
		# make this a singleton by calling UberSet = UberSet()
		return self

	def contains(self, obj):
		return True

	def union(self, set):
		return self

	def intersection(self, set):
		return set

	def difference(self, set):
		return self

	def symmetric_difference(self, set):
		return EmptySet

	def direct_product(self, set):
		return EmptySet

	def map(self, map_func, get_key=None):
		raise AssertionError, "An infinite set cannot be mapped"

	def add(self, obj):
		pass

	def remove(self, obj):
		pass

	def update(self,set):
		pass

	def intersection_update(self, set):
		pass

	def difference_update(self, set):
		pass

	def symmetric_difference_update(self, set):
		pass

	def count(self):
		raise AssertionError, "An infinite set cannot be counted"

	def __iter__(self):
		raise AssertionError, "An infinite set has no iterator"

	def __getitem__(self, key):
		pass

	def __setitem__(self, key, obj):
		pass

	def __delitem__(self, key):
		pass

	def __str__(self):
		return "{ * }"

	def __len__(self):
		raise AssertionError, "An infinite set has no length"

# EmptySet : the set of nothing (singleton)
EmptySet = EmptySet()

# UberSet: the set of everything (singleton)
UberSet = UberSet()

# Z : the set of all integers
Z = Set(expr=lambda x: isinstance(x, int))

# N : the set of all natural numbers
N = Set(expr=lambda x: isinstance(x, int) and x > 0)

# R : the set of all rational/real numbers
R = Set(expr=lambda x: isinstance(x, float))

# C : the set of all complex numbers
C = Set(expr=lambda x: isinstance(x, complex))

# S : the set of all sets
S = Set(expr=lambda x: isinstance(x, Set))

