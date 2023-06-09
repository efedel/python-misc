#!/usr/bin/env python

# TODO need a name -> id mapping

CPU_ARCH_MASK    = 0xff000000
CPU_ARCH_ABI64   = 0x01000000

CPU_TYPE_ANY     = -1
CPU_TYPE_VAX     = 1
CPU_TYPE_MC680x0 = 6
CPU_TYPE_X86     = 7
CPU_TYPE_I386    = CPU_TYPE_X86       
CPU_TYPE_MC98000 = 10
CPU_TYPE_HPPA    = 11
CPU_TYPE_MC88000 = 13
CPU_TYPE_SPARC   = 14
CPU_TYPE_I860    = 15
CPU_TYPE_POWERPC = 18
CPU_TYPE_POWERPC64=(CPU_TYPE_POWERPC | CPU_ARCH_ABI64)
