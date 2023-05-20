#!/usr/bin/env python

import binfile, fat

formats = ['fat']

def guessformat(self, buf):
    fat_magic = '\xca\xfe\xba\xbe'

    if buf[:4] == fat_magic:
        return 'fat'
    raise binfile.UnknownFileFormat, "Not a FAT binary."

def open(buf, format):
    if format != 'fat':
        raise binfile.UnknownFileFormat, "Only 'fat' is a supported format"
    return fat.FatArchive(buf)
