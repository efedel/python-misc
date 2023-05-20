#!/usr/bin/env python

import types

class BinaryObject(object):
    def __init__(self):
        self.load()
    def load(self):
        pass

class BinFile(BinaryObject):
    def __init__(self, buf):
        self.header = None
        self.segments = []
        self.segtable = {
            'code' : [],
            'data' : [],
            'strtab' : [],
            'symtab' : [],
            'reloc' : []
        }
        self.buf = str(buf[:])

        super(BinFile, self).__init__()

    def load(self):
        self._load_header()
        self._load_segments()

    def _load_header(self): pass
    def _load_segments(self): pass

    def code(self): return self.segtable['code']
    def data(self): return self.segtable['data']
    def strtab(self): return self.segtable['strtab']
    def symtab(self): return self.segtable['symtab']
    def relocs(self): return self.segtable['relocs']
    def __iadd__(self, other):
        import segment
        if not isinstance(other, segment.Segment):
            raise Exception, "%r is not a Segment" % other

        self.segments.append(other)
        if other.type in self.segtable:
            self.segtable[other.type].append(other)
        else:
            self.segtable[other.type] = [other]
        return self
    def __len__(self): return len(self.buf)
    __getitem__ = lambda s,k: s.buf[k]
    #def __getitem__(self, key): return self.buf[key]

class FileHeader(BinaryObject):
    entry = 0
    def __init__(self, struct):
        self.struct = struct
        super(FileHeader, self).__init__()

class BinArchive(BinaryObject):
    def __init__(self, struct, buf):
        self.struct = struct
        self.files = {}
        self.names = []
        self.buf = str(buf[:])
        super(BinArchive, self).__init__()
    def load(self):
        self._load_files()
    def contents(self):
        return self.files.iteritems()
    def __iadd__(self, file):
        self.files[file.name] = file
        return self
    def __getitem__(self, name):
        if type(name) in (types.SliceType, types.IntType, types.LongType):
            return self.buf[name]
        return self.files[name]
    def __len__(self):
        return len(self.buf)

class ArchiveMember(BinaryObject):
    name = None
    offset = None
    size = None
    def __init__(self, container, struct):
        self.container = container
        self.struct = struct
        super(ArchiveMember, self).__init__()
    def load(self):
        off, size = self.offset, self.size
        self.buf = self.container[off:off+size]
        super(ArchiveMember, self).load()

    def __len__(self):
        return self.size

class UnknownFileFormat(Exception):
    pass
