#!/usr/bin/env python

# vim regex for #define Immediate
# /#define \([A-Z_]*\)\s*\([0-9]*\)\s*\(.*$\)/

#import binfile
from structure import *

EI_NIDENT   = 16
ELFMAG      = "\177ELF"

EI_CLASS    = 4
ELFCLASSNONE= 0
ELFCLASS32  = 1
ELFCLASS64  = 2

EI_DATA     = 5
ELFDATANONE = 0
ELFDATA2LSB = 1
ELFDATA2MSB = 2

EI_VERSION  = 6
EI_OSABI    = 7
EI_ABIVERSION=8
EI_PAD      = 9

PT_NULL        =0 
PT_LOAD        =1
PT_DYNAMIC     =2
PT_INTERP      =3
PT_NOTE        =4
PT_SHLIB       =5
PT_PHDR        =6
PT_TLS         =7

PF_X        = (1<<0)
PF_W        = (1<<1)
PF_R        = (1<<2)

SHT_NULL         =0
SHT_PROGBITS     =1
SHT_SYMTAB       =2
SHT_STRTAB       =3
SHT_RELA         =4
SHT_HASH         =5
SHT_DYNAMIC      =6
SHT_NOTE         =7
SHT_NOBITS       =8
SHT_REL          =9
SHT_SHLIB        =10
SHT_DYNSYM       =11
SHT_INIT_ARRAY   =14
SHT_FINI_ARRAY   =15
SHT_PREINIT_ARRAY=16
SHT_GROUP        =17
SHT_SYMTAB_SHNDX =18

SHF_WRITE           =(1 << 0)
SHF_ALLOC           =(1 << 1)
SHF_EXECINSTR       =(1 << 2)
SHF_MERGE           =(1 << 4)
SHF_STRINGS         =(1 << 5)
SHF_INFO_LINK       =(1 << 6)
SHF_LINK_ORDER      =(1 << 7)
SHF_OS_NONCONFORMING=(1 << 8)
SHF_GROUP           =(1 << 9)
SHF_TLS             =(1 << 10)


class ElfEhdr(Structure):
    pass

class Elf32Ehdr(ElfEhdr):
    __struct__ = (
        ('e_ident',         uInt8 * EI_NIDENT),
        ('e_type',          uInt16),
        ('e_machine',       uInt16),
        ('e_version',       uInt32),
        ('e_entry',         uInt32),
        ('e_phoff',         uInt32),
        ('e_shoff',         uInt32),
        ('e_flags',         uInt32),
        ('e_ehsize',        uInt16),
        ('e_phentsize',     uInt16),
        ('e_phnum',         uInt16),
        ('e_shentsize',     uInt16),
        ('e_shnum',         uInt16),
        ('e_shstrndx',      uInt16)
    )

class Elf64Ehdr(ElfEhdr):
    __struct__ = (
        ('e_ident',         uInt8 * EI_NIDENT),
        ('e_type',          uInt16),
        ('e_machine',       uInt16),
        ('e_version',       uInt32),
        ('e_entry',         uInt64),
        ('e_phoff',         uInt64),
        ('e_shoff',         uInt64),
        ('e_flags',         uInt32),
        ('e_ehsize',        uInt16),
        ('e_phentsize',     uInt16),
        ('e_phnum',         uInt16),
        ('e_shentsize',     uInt16),
        ('e_shnum',         uInt16),
        ('e_shstrndx',      uInt16)
    )

class ElfShdr(Structure):
    pass

class Elf32Shdr(ElfShdr):
    __struct__ = (
        ('sh_name',         uInt32),
        ('sh_type',         uInt32),
        ('sh_flags',        uInt32),
        ('sh_addr',         uInt32),
        ('sh_offset',       uInt32),
        ('sh_size',         uInt32),
        ('sh_link',         uInt32),
        ('sh_info',         uInt32),
        ('sh_addralign',    uInt32),
        ('sh_entsize',      uInt32),
    )

class Elf64Shdr(ElfShdr):
    __struct__ = (
        ('sh_name',         uInt32),
        ('sh_type',         uInt32),
        ('sh_flags',        uInt64),
        ('sh_addr',         uInt64),
        ('sh_offset',       uInt64),
        ('sh_size',         uInt64),
        ('sh_link',         uInt32),
        ('sh_info',         uInt32),
        ('sh_addralign',    uInt64),
        ('sh_entsize',      uInt64),
    )

class ElfPhdr(Structure):
    pass

class Elf32Phdr(ElfPhdr):
    __struct__ = (
        ('p_type',      uInt32),
        ('p_offset',    uInt32),
        ('p_vaddr',     uInt32),
        ('p_paddr',     uInt32),
        ('p_filesz',    uInt32),
        ('p_memsz',     uInt32),
        ('p_flags',     uInt32),
        ('p_align',     uInt32)
    )

class Elf64Phdr(ElfPhdr):
    __struct__ = (
        ('p_type',      uInt32),
        ('p_flags',     uInt32),
        ('p_offset',    uInt64),
        ('p_vaddr',     uInt64),
        ('p_paddr',     uInt64),
        ('p_filesz',    uInt64),
        ('p_memsz',     uInt64),
        ('p_align',     uInt64)
    )

class ElfSym(Structure):
    pass

class Elf32Sym(ElfSym):
    __struct__ = (
        ('st_name',     uInt32),
        ('st_value',    uInt32),
        ('st_size',     uInt32),
        ('st_info',     uInt8),
        ('st_other',    uInt8),
        ('st_shndx',    uInt16),
    )

class Elf64Sym(ElfSym):
    __struct__ = (
        ('st_name',     uInt32),
        ('st_info',     uInt8),
        ('st_other',    uInt8),
        ('st_shndx',    uInt16),
        ('st_value',    uInt64),
        ('st_size',     uInt64),
    )

STB_GLOBAL      = 1     # /* Global symbol */
STB_WEAK        = 2     # /* Weak symbol */
STB_NUM         = 3     # /* Number of defined types.  */
STB_LOOS        = 10    # /* Start of OS-specific */
STB_HIOS        = 12    # /* End of OS-specific */
STB_LOPROC      = 13    # /* Start of processor-specific */
STB_HIPROC      = 15    # /* End of processor-specific */

STT_NOTYPE      = 0     # /* Symbol type is unspecified */
STT_OBJECT      = 1     # /* Symbol is a data object */
STT_FUNC        = 2     # /* Symbol is a code object */
STT_SECTION     = 3     # /* Symbol associated with a section */
STT_FILE        = 4     # /* Symbol's name is file name */
STT_COMMON      = 5     # /* Symbol is a common data object */
STT_TLS         = 6     # /* Symbol is thread-local data object*/
STT_NUM         = 7     # /* Number of defined types.  */
STT_LOOS        = 10    # /* Start of OS-specific */
STT_HIOS        = 12    # /* End of OS-specific */
STT_LOPROC      = 13    # /* Start of processor-specific */
STT_HIPROC      = 15    # /* End of processor-specific */

STN_UNDEF       = 0

ELF_ST_VISIBILITY=ELF32_ST_VISIBILITY=ELF64_ST_VISIBILITY = lambda o: (o&0x3)

STV_DEFAULT     = 0     # /* Default symbol visibility rules */
STV_INTERNAL    = 1     # /* Processor specific hidden class */
STV_HIDDEN      = 2     # /* Sym unavailable in other modules */
STV_PROTECTED   = 3     # /* Not preemptible, not exported */

class ElfSymInfo(Structure):
    pass

class Elf32SymInfo(ElfSymInfo):
    __struct__ = (
        ('si_boundto',  uInt16),
        ('si_flags',    uInt16),
    )

class Elf64SymInfo(ElfSymInfo):
    __struct__ = (
        ('si_boundto',  uInt16),
        ('si_flags',    uInt16),
    )

SYMINFO_BT_SELF        =0xffff
SYMINFO_BT_PARENT      =0xfffe
SYMINFO_BT_LOWRESERVE  =0xff00
                                                     
SYMINFO_FLG_DIRECT      =0x0001
SYMINFO_FLG_PASSTHRU    =0x0002
SYMINFO_FLG_COPY        =0x0004
SYMINFO_FLG_LAZYLOAD    =0x0008

SYMINFO_NONE            =0                    
SYMINFO_CURRENT         =1                    
SYMINFO_NUM             =2                    
                                                     
ELF_ST_BIND = ELF32_ST_BIND = ELF64_ST_BIND = lambda val: (val & 0xF0) >> 4
ELF_ST_TYPE = ELF32_ST_TYPE = ELF64_ST_TYPE = lambda val: (val & 0x0F)
ELF_ST_INFO = ELF32_ST_INFO = ELF64_ST_INFO =lambda bind, type: ((bind << 4) & 0xF0) | (type & 0x0F)
