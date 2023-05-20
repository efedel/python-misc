#!/usr/bin/env python

import binfile, perms

# a region is a subportion of a binary file
# containing a limited set of core data values
# a segment is a region with an interpretation

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
        self.load()
    def load(self):
        pass # setup the core values from the structure...

class Region(binfile.BinaryObject):
    def __init__(self, binfile, header):
        self.binfile = binfile
        self.header = header
    def __getitem__(self, key):
        import types
        if type(key) == types.SliceType:
            fail = False

            if len(key) == 2:
                start, stop = key
            elif len(key) == 1:
                start, stop = key, key
            else:
                raise IndexError, "Slice '%r' is not supported" % key

            if stop > self.header.size:
                fail = True
            elif stop - start > self.header.size:
                fail = True
            elif start > self.header.size:
                fail = True

            if fail:
                raise IndexError, "Range '%r' is out of bounds" % key

            rv = self.binfile[self.header.offset+start:self.header.offset+stop]
        else:
            rv = self.binfile[key]
        return rv
    def __len__(self):
        return self.header.size
