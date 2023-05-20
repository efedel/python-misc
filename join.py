#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs 
subject = 'a fred'
word =  u'абвгдеёжзийклмно' 
rating = "5.0"
subject_age = '60'
subject_sex = 'M'
WAVE_OUTPUT_FILENAME = 'wav.out'

#line = '|'.join( [subject, word, rating, subject_age, subject_sex, WAVE_OUTPUT_FILENAME])
line = [subject, word, rating, subject_age, subject_sex, WAVE_OUTPUT_FILENAME]

f = codecs.open('/tmp/unicode_test.txt', encoding='utf-8', mode='w')
f.write(line)
f.write("\n")
f.close
