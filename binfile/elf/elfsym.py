#!/usr/bin/env python

import segment

# parse PLT

# requie rva_to_offset / offset_to_rva

class ElfSymTab(segment.SymTab):
    # self.header.shdr
    def _load_symbols(self, struct):
        read_symbol_structs()
        get_strtab_segment()

        for sym in symstructs:
            name = strtab[sym.st_name]
            rva = sym.st_value

class ElfSymbol(segment.Symbol):
    def load(self):
