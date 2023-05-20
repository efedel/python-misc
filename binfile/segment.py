#!/usr/bin/env python

import binfile, perms

CODE = 'code'
DATA = 'data'
STRTAB = 'strtab'
SYMTAB = 'symtab'
RELOC = 'reloc'
UNKNOWN = 'unknown'

class SegmentHeader(binfile.BinaryObject):
    rva = 0
    offset = 0
    struct = None
    size = 0
    perms = None
    def __init__(self, struct):
        self.struct = struct
        if not self.perms:
            self.perms = perms.Perms()
        super(SegmentHeader, self).__init__()

class Segment(binfile.BinaryObject):
    type = UNKNOWN
    region = []
    def __init__(self, binfile, header):
        self.binfile = binfile
        self.header = header
        self.region = buffer(binfile.buf, header.offset, header.size)
        super(Segment, self).__init__()
    def __getitem__(self, key):
        return self.region[key]
    def __len__(self):
        return self.header.size

class Code(Segment): type = CODE
class Data(Segment): type = DATA

class StrTab(Segment):
    type = STRTAB
    NUL = '\x00'
    def __getitem__(self, key):
        import types, struct

        ktype = type(key)
        if ktype == types.SliceType:
            if key.step:
                raise IndexError, 'Unsupported slice range: %r' % key
            start, stop = key.start, key.stop
        elif ktype == types.IntType or ktype == types.LongType:
            start = key
            # TODO check if this is really needed, maybe 's' is sufficient
            ndx = self.region[start:].find(self.NUL)
            if ndx != -1:
                stop = start + ndx
            else:
                stop = self.header.size
        else:
            raise IndexError, 'Illegal index value: %r' % key
        cnt = stop - start
        #rv = struct.unpack(str(cnt) + 's', self.region[start:stop])[0]
        rv = self.region[start:stop]
        return rv

class SymTab(Segment):
    type = SYMTAB
    def __init__(self, *args, **kwargs):
        self.table = {}
        super(SymTab, self).__init__(*args, **kwargs)

    def load(self):
        for sym in self._load_symbols():
            self.table[ sym.name ] = sym

    def _load_symbols(self, struct, symbol, entsize=None):
        from structure import extract_struct_list

        if not entsize:
            entsize = len(struct())
        cnt = self.header.size / entsize
        buf = self.region

        return [symbol(s) for s in extract_struct_list(buf,struct,cnt,entsize)]

    def keys(self): return self.table.keys()
    def iteritems(self): return self.table.iteritems()
    def values(self): return self.table.values()
    def __getitem__(self, key): return self.table[key]
    def __len__(self): return len(self.table)

# new file content below
class Symbol(binfile.BinaryObject):
    name = ''
    rva = 0
    def __init__(self, struct):
        self.struct = struct
        super(Symbol, self).__init__()

class Relocs(binfile.BinaryObject):
    pass # wtf#@!... list of relocations
