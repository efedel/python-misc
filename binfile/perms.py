#!/usr/bin/env python

import operator, types

_R = (1 << 0)
_W = (1 << 1)
_X = (1 << 2)

def _permstr_to_int(permstr):
    invert = False
    rv = 0
    if len(permstr) > 1:
        if permstr[0] == '~' or permstr[0] == '!':
            invert = True
            permstr = permstr[1:]
    for c in permstr:
        if   c == 'r': rv |= _R
        elif c == 'w': rv |= _W
        elif c == 'x': rv |= _X
        elif c == '-': continue
        else:
            raise Exception, "Bad permission string: %s" % permstr
    if invert:
        rv = operator.invert(rv)
    return rv

def _int_to_permstr(iperm):
    rv = ['-', '-', '-']
    if iperm & _R: rv[0] = 'r'
    if iperm & _W: rv[1] = 'w'
    if iperm & _X: rv[2] = 'x'
    return ''.join(rv)

class Perms(object):
    _val = 0
    isread  = lambda s: operator.truth( s._val & _R )
    iswrite = lambda s: operator.truth( s._val & _W )
    isexec  = lambda s: operator.truth( s._val & _X )
    def __init__(self, permstr=''):
        if permstr:
            self._val = _permstr_to_int(permstr)
    def __ior__(self, other):
        other = _permstr_to_int(other)
        self._val = operator.or_(self._val, other)
        return self
    def __iand__(self, other):
        other = _permstr_to_int(other)
        self._val = operator.and_(self._val, other)
        return self
    def __ixor__(self, other):
        other = _permstr_to_int(other)
        self._val = operator.xor(self._val, other)
        return self
    def __or__(self, other):
        other = _permstr_to_int(other)
        v = operator.or_(self._val, other)
        return Perms(_int_to_permstr(v))
    def __and__(self, other):
        other = _permstr_to_int(other)
        v = operator.and_(self._val, other)
        return Perms(_int_to_permstr(v))
    def __xor__(self, other):
        other = _permstr_to_int(other)
        v = operator.xor(self._val, other)
        return Perms(_int_to_permstr(v))
    def __eq__(self, other):
        if type(other) == types.StringType:
            other = _permstr_to_int(other)
        elif other.__class__ == self.__class__:
            other = other._val
        else:
            raise Exception, "Can't compare Permission object to: %r" % other
        return self._val == other
    def __contains__(self, other):
        rv = 0
        for c in other:
            if   c == 'r': rv |= self._val & _R
            elif c == 'w': rv |= self._val & _W
            elif c == 'x': rv |= self._val & _X
            elif c == '-': continue
            else:
                raise Exception, "Bad permission string: %s" % permstr
        return rv
    def __str__(self):
        return _int_to_permstr(self._val)
    def __repr__(self):
        return '%s("%s")'%(self.__class__.__name__, _int_to_permstr(self._val))
