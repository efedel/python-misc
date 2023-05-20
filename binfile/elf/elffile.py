#!/usr/bin/env python

import binfile, segment
from elfstructs import *

class ElfFile(binfile.BinFile):
    def __init__(self, *args, **kwargs):
        self.sections = {}
        super(ElfFile, self).__init__(*args, **kwargs)

    def _load_header(self, ehdr):
        self.ehdr = ehdr(self.buf[:len(ehdr())])
        self.header = ElfFileHeader(self.ehdr)
        self.entry = self.header.entry
        super(ElfFile, self)._load_header()

    def _load_segments(self, shdr, phdr):
        from structure import extract_struct_list

        ehdr = self.ehdr

        if len(shdr()) != ehdr.e_shentsize or \
           len(phdr()) != ehdr.e_phentsize:
               raise Warning, 'ELF has corrupt header entry sizes'

        self.shdrs = extract_struct_list(self.buf[ehdr.e_shoff:],
                shdr, ehdr.e_shnum)
        self.phdrs = extract_struct_list(self.buf[ehdr.e_phoff:],
                phdr, ehdr.e_phnum)

        self._load_shsegments()
        self._load_phsegments()

        super(ElfFile, self)._load_segments()

    def _load_shsegments(self):
        def init_names(seglist):
            if self.ehdr.e_shstrndx > 0 and \
               self.ehdr.e_shstrndx < len(self.shdrs):
                strshdr = self.shdrs[self.ehdr.e_shstrndx]
            else:
                return

            strtab = None
            for seg in seglist:
                if seg.header.struct == strshdr:
                    strtab = seg

            if not strtab:
                return

            for seg in seglist:
                 setattr(seg, 'name', strtab[seg.header.struct.sh_name])

        def make_segments():
            sl = []
            for shdr in self.shdrs:
                seghdr = ElfShSegmentHeader(shdr)

                shtype = shdr.sh_type

                if shtype == SHT_PROGBITS:
                    if seghdr.perms | 'x':
                        seg = segment.Code( self, seghdr )
                    else:
                        seg = segment.Data( self, seghdr )
                elif shtype in (SHT_SYMTAB, SHT_DYNSYM):
                    seg = ElfSymTab( self, seghdr )
                elif shtype == SHT_STRTAB:
                    seg = segment.StrTab( self, seghdr )
                # elif shtype in (SHT_REL, SHT_RELA):
                #   seg = ElfRelocs( self, seghdr )
                else:
                    seg = segment.Segment(self, seghdr)
                sl.append(seg)
            return sl
        seglist = make_segments()
        init_names( seglist )

        for seg in seglist:
            self += seg
            if seg.name:
                self.sections[seg.name] = seg

    def _load_phsegments(self):
        for phdr in self.phdrs:
            seghdr = ElfPhSegmentHeader(phdr)

            if phdr.p_type == PT_LOAD:
                if seghdr.perms == 'r-x':
                    self += segment.Code(self, seghdr)
                else:
                    self += segment.Data(self, seghdr)
            else:
                self += segment.Segment(self, seghdr)

class Elf32File(ElfFile):
    def _load_header(self):
        super(Elf32File, self)._load_header(Elf32Ehdr)
    def _load_segments(self):
        super(Elf32File, self)._load_segments(Elf32Shdr, Elf32Phdr)

class Elf64File(ElfFile):
    def _load_header(self):
        super(Elf64File, self)._load_header(Elf64Ehdr)
    def _load_segments(self):
        super(Elf64File, self)._load_segments(Elf64Shdr, Elf64Phdr)

class ElfFileHeader(binfile.FileHeader):
    def load(self):
        self.entry = self.struct.e_entry

class ElfShSegmentHeader(segment.SegmentHeader):
    name = ''
    def load(self):
        self.shdr = self.struct
        self.rva = self.shdr.sh_addr
        self.offset = self.shdr.sh_offset
        self.size = self.shdr.sh_size

        self.perms |= 'r'
        if self.shdr.sh_flags & SHF_WRITE: self.perms |= 'w'
        if self.shdr.sh_flags & SHF_EXECINSTR: self.perms |= 'x'

class ElfPhSegmentHeader(segment.SegmentHeader):
    def load(self):
        self.phdr = self.struct
        self.rva = self.phdr.p_vaddr
        self.offset = self.phdr.p_offset
        self.size = self.phdr.p_filesz

        if self.phdr.p_flags & PF_R: self.perms |= 'r'
        if self.phdr.p_flags & PF_W: self.perms |= 'w'
        if self.phdr.p_flags & PF_X: self.perms |= 'x'

class ElfSymTab(segment.SymTab):
    def _load_symbols(self):
        return []
