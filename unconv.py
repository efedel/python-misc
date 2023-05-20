#!/usr/bin/env python
# text conversion from code a to codec b
# -*- coding: utf-8 -*-

import codecs
str = u'абвгдеёжзийклмно'

f = codecs.open('a.txt', mode='r')
line = f.readline()
f.close

#print(unicode(line))

str = line.decode('unicode-escape')
print('\u0441'.decode('unicode-escape'))

#print '\u84b8\u6c7d\u5730'.decode('unicode-escape')

str = u"%s" % line

print(str.encode('utf-8'))


f = codecs.open('b.txt', encoding='utf-8', mode='w')
#f.write(str.encode('utf-8'))
f.write(line.decode('unicode-escape'))
f.write("\n")
f.close

