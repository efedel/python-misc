#!/usr/bin/python

f = open('bgo_schema.sql')
lines = f.readlines()
for i in lines:
	print i
f.close()

