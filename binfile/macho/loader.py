#!/usr/bin/env python

from structure import *

MH_MAGIC = 0xfeedface
MH_MAGIC_64 = 0xfeedfacf

class MachHeaderStruct(Structure):
    __struct__ = (
        ('magic',       uInt32),
        ('cputype',     Int32),
        ('cpusubtype',  Int32),
        ('filetype',    uInt32),
        ('ncmds',       uInt32),
        ('sizeofcmds',  uInt32),
        ('flags',       uInt32),
    )


class MachHeader64Struct(Structure):
    __struct__ = (
        ('magic',       uInt32),
        ('cputype',     Int32),
        ('cpusubtype',  Int32),
        ('filetype',    uInt32),
        ('ncmds',       uInt32),
        ('sizeofcmds',  uInt32),
        ('flags',       uInt32),
        ('reserved',       uInt32),
    )

class LoadCommandStruct(Structure):
    __struct__ = (
        ('cmd',     uInt32),
        ('cmdsize', uInt32),
    )
    # essentially, Mach-O is a TLV style format...

def read_load_commands(buf, ncmds):
    off = 0
    rl = []
    for i in range(ncmds):
        rl.append( LoadCommandStruct(buf[off:]) )
        off += rl[-1].cmdsize
    return rl

