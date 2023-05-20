#!/usr/bin/env python

# convert from MS header file format to __struct__ format 
# : {RANGE} /\<\([^ ]*\)\>[ ]*\<\([^ ]*\)\>/('\2', \1),/

from structure import *
import binfile

IMAGE_DOS_SIGNATURE = "MZ"

class IMAGE_DOS_HEADER(Structure):
    __struct__ = (
        ('e_magic',     uInt8 * 2),
        ('e_cblp',      uInt16),
        ('e_cp',        uInt16),
        ('e_cric',      uInt16),
        ('e_cparhdr',   uInt16),
        ('e_minalloc',  uInt16),
        ('e_maxalloc',  uInt16),
        ('e_ss',        uInt16),
        ('e_sp',        uInt16),
        ('e_csum',      uInt16),
        ('e_ip',        uInt16),
        ('e_cs',        uInt16),
        ('e_lfarlc',    uInt16),
        ('e_ovno',      uInt16),
        ('e_res',       uInt16 * 4),
        ('e_oemid',     uInt16),
        ('e_oeminfo',   uInt16),
        ('e_res2',      uInt16 * 10),
        ('e_lfanew',    uInt32),
    )

class IMAGE_FILE_HEADER(Structure):
    __struct__ = (
        ('Machine',     uInt16),
        ('NumberOfSections',    uInt16),
        ('TimeDateStamp',   uInt32),
        ('PointerToSymbolTable', uInt32),
        ('NumberOfSymbols', uInt32),
        ('SizeOfOptionalHeader', uInt16),
        ('Characteristics', uInt16),
    )

class IMAGE_DATA_DIRECTORY(Structure):
    __struct__ = (
        ('VirtualAddress',  uInt32),
        ('Size',        uInt32),
    )

IMAGE_NUMBEROF_DIRECTORY_ENTRIES = 16

class IMAGE_OPTIONAL_HEADER(Structure):
    __struct__ = (
        ('Magic', uInt16),
        ('MajorLinkerVersion', uInt8),
        ('MinorLinkerVersion', uInt8),
        ('SizeOfCode', uInt32),
        ('SizeOfInitializedData', uInt32),
        ('SizeOfUninitializedData', uInt32),
        ('AddressOfEntryPoint', uInt32),
        ('BaseOfCode', uInt32),
        ('BaseOfData', uInt32),
        ('ImageBase', uInt32),
        ('SectionAlignment', uInt32),
        ('FileAlignment', uInt32),
        ('MajorOperatingSystemVersion', uInt16),
        ('MinorOperatingSystemVersion', uInt16),
        ('MajorImageVersion', uInt16),
        ('MinorImageVersion', uInt16),
        ('MajorSubsystemVersion', uInt16),
        ('MinorSubsystemVersion', uInt16),
        ('Win32VersionValue', uInt32),
        ('SizeOfImage', uInt32),
        ('SizeOfHeaders', uInt32),
        ('CheckSum', uInt32),
        ('Subsystem', uInt16),
        ('DllCharacteristics', uInt16),
        ('SizeOfStackReserve', uInt32),
        ('SizeOfStackCommit', uInt32),
        ('SizeOfHeapReserve', uInt32),
        ('SizeOfHeapCommit', uInt32),
        ('LoaderFlags', uInt32),
        ('NumberOfRvaAndSizes', uInt32),
    )
    DataDirectory = []

    def _unpack(self, buf):
        super(IMAGE_OPTIONAL_HEADER, self)._unpack(buf)

        # ... range(offset_of(DataDirectory), sizeof(DataDirectory),
        #                                       sizeof(DirectoryEntry) )
        for loc in range(96, 224, 8):
            self.DataDirectory.append(IMAGE_DATA_DIRECTORY(buf[loc:loc+8]))

    def __len__(self):
        return 224

class IMAGE_NT_HEADERS(Structure):
    __struct__ = (
        ('Signature',       uInt32),
    )
    FileHeader = None
    OptionalHeader = None

    def _unpack(self, buf):
        super(IMAGE_NT_HEADERS, self)._unpack(buf)
        self.FileHeader = IMAGE_FILE_HEADER(buf[4:])
        self.OptionalHeader = IMAGE_OPTIONAL_HEADER(buf[4+len(self.FileHeader):])

    def __len__(self):
        return 4 + len(self.FileHeader) + len(self.OptionalHeader)

class IMAGE_SECTION_HEADER(Structure):
    __struct__ = (
        ('Name', StrBuf(8)),
        ('PhysicalAddress', uInt32),
        ('VirtualAddress', uInt32),
        ('SizeOfRawData', uInt32),
        ('PointerToRawData', uInt32),
        ('PointerToRelocations', uInt32),
        ('PointerToLinenumbers', uInt32),
        ('NumberOfRelocations', uInt16),
        ('NumberOfLinenumbers', uInt16),
        ('Characteristics', uInt32),
    )

    VirtualSize = 0

    def _unpack(self, buf):
        super(IMAGE_SECTION_HEADER, self)._unpack(buf)
        self.VirtualSize = self.PhysicalAddress

def IMAGE_FIRST_SECTION(ntheader):
    return buf[ntheader.OptionalHeader + len(ntheader.OptionalHeader):]

class PeFile(binfile.BinFile):
    pass
