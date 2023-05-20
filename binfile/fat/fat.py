#!/usr/bin/env python2.5

import binfile, fat_h, machine_h

def cpumime2name(cputype, cpusubtype):
    if cputype == machine_h.CPU_TYPE_I386:
        return "i386"
    return "ppc"

def name2cpumime(name):
    pass

class FatArchive(binfile.BinArchive):
    def __init__(self, buf):
        struct = fat_h.fat_header(buf)
        if struct.magic != fat_h.FAT_MAGIC:
            raise binfile.UnknownBinaryFormat, 'bad Fat magic numer: %x' % \
                    struct.magic
        super(FatArchive, self).__init__(struct, buf)
    def _load_files(self):
        off = len(self.struct)
        for i in range(self.struct.nfat_arch):
            self += FatMember(self, fat_h.fat_arch(self.buf[off:]))
            off += len(fat_h.fat_arch())

class FatMember(binfile.ArchiveMember):
    def load(self):
        self.offset = self.struct.offset
        self.size = self.struct.size
        self.name = cpumime2name(self.struct.cputype, self.struct.cpusubtype)
        super(FatMember, self).load()
