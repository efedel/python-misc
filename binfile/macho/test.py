#!/usr/bin/env python

from structure import extract_struct_list

import fat
import loader
import machines

class FatBinary(object):
    def __init__(self, buf):
        self.data = buf
        self.load()

    def load(self):
        buf = self.data
        self.header = fat.FatHeaderStruct(buf)
        self.archs = extract_struct_list(buf[len(self.header):], 
                fat.FatArchStruct, self.header.nfat_arch, 
                len(fat.FatArchStruct()))

        self.table = {}
        for arch in self.archs:
            self.table[(arch.cputype,arch.cpusubtype)] = arch

def get_buf():
    return open("/Users/thegrugq/src/bgo/binfile/testbin/sidenote").read()
