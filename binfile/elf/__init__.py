#!/usr/bin/env python

from elf_h import EI_NIDENT as _EI_NIDENT
from elf_h import EI_CLASS as _EI_CLASS
from elf_h import ELFMAG as _ELFMAG
from elf_h import ELFCLASS32 as _ELFCLASS32 
from elf_h import ELFCLASS64 as _ELFCLASS64

from elf import Elf32File, Elf64File
import binfile

formats = ['elf', 'elf32', 'elf64']

def guessformat(buf):
    if len(buf) < _EI_NIDENT:
        raise binfile.UnknownFileFormat, "Too small to [%d] to be an ELF" %\
                len(buf)
    if buf[:len(_ELFMAG)] != _ELFMAG:
        raise binfile.UnknownFileFormat, "Bad magic number: %r" % \
                buf[:len(SELF_MAG)]

    c = ord( buf[ _EI_CLASS ] )
    if c == _ELFCLASS32:
        format = 'elf32'
    elif c == _ELFCLASS64:
        format = 'elf64'
    else:
        raise binfile.UnknownFileFormat, "Unsupported ELF class (%d)" % c
    return format

def open(buf, format):
    if format == 'elf':
        format = guessformat(buf)

    if format == 'elf32':
        ElfFile = Elf32File
    elif format == 'elf64':
        ElfFile = Elf64File
    else:
        raise binfile.UnknownFileFormat, "ELF doesn't support: %s" % format
    return ElfFile(buf)
